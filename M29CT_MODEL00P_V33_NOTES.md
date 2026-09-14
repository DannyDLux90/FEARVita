# M29CT Model00p v33 renderer notes (WIP)

Public reference: haekb/io_scene_lithtech PR #24 `src/reader_model00p_pc.py`.

FEAR v33 MeshData is 64 bytes: position3f, normal3f, uv2f, two extra float3 vectors, weight_info[3], pad, node_indexes[3], pad. MeshInfo has start/count/size/index-position/unknown/triangle-count/material-index/influence-count/unknown + influence-node list. Indices are uint16 global mesh-data indexes and become local by subtracting mesh_data_start. Weights are byte/255 and map node indexes through the MeshInfo influence list.

IMPORTANT: the prior live session's native Model00p renderer code was not persisted before the workspace reset. Rebuild it from these notes/reference; do not claim 0.42 release-ready until restored and tested.
