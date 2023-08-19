header = ["SName", "Position", "Rotation", "Scale"]  # 表头
name = inst.object.name
                        
#获取矩阵变换数据
matrix = inst.matrix_world
translation, rotation, scale = matrix.decompose()


rows.append([name,translation, rotation, scale])