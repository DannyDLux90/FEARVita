# Reconstruct the M29DH worktree patch

```bash
cat patches/M29DH_CURRENT_WORKTREE.patch.gz.b64.part* | base64 -d > M29DH_CURRENT_WORKTREE.patch.gz
sha256sum M29DH_CURRENT_WORKTREE.patch.gz
# expected SHA-256 is stored in patches/M29DH_CURRENT_WORKTREE.patch.gz.sha256
gunzip M29DH_CURRENT_WORKTREE.patch.gz
```

The patch is the exact tracked `git diff HEAD` from the local reconstructed M29CU base (`d049583`) to the M29DH workspace snapshot.
