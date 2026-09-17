#include "fearvita/vita2d_pool_budget.h"

#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>

namespace {

void Require(bool condition, const char* message) {
  if (!condition) {
    std::cerr << message << '\n';
    std::exit(1);
  }
}

// Model the allocator contract from libvita2d a8f15ab, independently of the
// conservative budget calculation. This allocator must reject exact fits.
bool TryAllocate(std::size_t capacity, std::size_t& used,
                 std::size_t bytes, std::size_t alignment) {
  const std::size_t aligned = (used + alignment - 1u) & ~(alignment - 1u);
  if (aligned >= capacity || bytes >= capacity - aligned) return false;
  used = aligned + bytes;
  return true;
}

}  // namespace

int main() {
  using fearvita::HasVita2dVertexPoolSpace;

  // The old checks could fit vertices but leave only four bytes for the
  // unguarded 16-byte libvita2d color uniform.
  Require(!HasVita2dVertexPoolSpace(64, 3, 20, true),
          "A textured draw must budget its color uniform");
  Require(!HasVita2dVertexPoolSpace(94, 3, 20, true),
          "Worst-case exact fits must be rejected");
  Require(HasVita2dVertexPoolSpace(95, 3, 20, true),
          "One byte beyond the conservative bound must fit");
  Require(!HasVita2dVertexPoolSpace(63, 3, 16, false),
          "Color vertex allocation must reserve alignment and strict end");
  Require(HasVita2dVertexPoolSpace(64, 3, 16, false),
          "A safely fitting color draw must be accepted");

  Require(!HasVita2dVertexPoolSpace(1024, 0, 20, true), "Reject empty draws");
  Require(!HasVita2dVertexPoolSpace(1024, 3, 0, true), "Reject zero stride");
  Require(!HasVita2dVertexPoolSpace(
              std::numeric_limits<std::size_t>::max(),
              std::numeric_limits<std::size_t>::max(), 20, true),
          "Reject overflowing vertex byte counts");
  Require(!HasVita2dVertexPoolSpace(
              std::numeric_limits<std::size_t>::max(),
              std::numeric_limits<unsigned int>::max(), 20, true),
          "Reject sizes that truncate at the Vita allocator boundary");

  // 120,000 textured triangles require 7.2 MB of actual GPU vertices, which
  // fits in the existing 8 MiB pool once CPU projection scratch is separate.
  Require(HasVita2dVertexPoolSpace(8u * 1024u * 1024u, 360000u, 20u, true),
          "The geometry budget must fit without the duplicate pool copy");

  std::size_t checked = 0;
  for (std::size_t initial = 0; initial != 32; ++initial) {
    for (std::size_t free_bytes = 0; free_bytes != 513; ++free_bytes) {
      for (std::size_t count = 1; count != 25; ++count) {
        for (bool textured : {false, true}) {
          const std::size_t stride = textured ? 20u : 16u;
          if (!HasVita2dVertexPoolSpace(free_bytes, count, stride, textured))
            continue;
          std::size_t used = initial;
          const std::size_t capacity = initial + free_bytes;
          Require(TryAllocate(capacity, used, count * stride, 16),
                  "Accepted draw exhausted the pool on vertices");
          if (textured) {
            Require(TryAllocate(capacity, used, 16, 4),
                    "Accepted draw exhausted the pool on the hidden uniform");
          }
          ++checked;
        }
      }
    }
  }

  std::cout << "PASS: " << checked
            << " accepted draw layouts satisfy the libvita2d contract\n";
  return 0;
}
