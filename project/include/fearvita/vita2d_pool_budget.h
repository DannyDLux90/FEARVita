#pragma once

#include <cstddef>
#include <cstdint>
#include <limits>

namespace fearvita {

// libvita2d uses an unsigned-int allocator and rejects allocations whose end
// equals pool_size. Reserve worst-case alignment padding before every hidden
// pool allocation as well as the RGBA uniform used by textured draws.
// CPU-only projection scratch is deliberately not allocated from this pool.
inline bool HasVita2dVertexPoolSpace(std::size_t free_bytes,
                                     std::size_t vertex_count,
                                     std::size_t vertex_stride,
                                     bool textured) {
  const std::size_t max_allocation =
      std::numeric_limits<unsigned int>::max();
  if (vertex_count == 0 || vertex_stride == 0 ||
      vertex_stride > max_allocation ||
      vertex_count > max_allocation / vertex_stride) {
    return false;
  }

  const std::uint64_t vertex_bytes =
      static_cast<std::uint64_t>(vertex_count) * vertex_stride;
  const std::uint64_t required =
      vertex_bytes + 15u + (textured ? 3u + 16u : 0u);
  return required < static_cast<std::uint64_t>(free_bytes);
}

}  // namespace fearvita
