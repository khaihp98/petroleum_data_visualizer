import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from obspy.io.segy.segy import _read_segy
# from mayavi import mlab    # import mlab
import pyvista as pv

filename = 'C:/Users/Admin/Downloads/Kerry3D.segy'
raw = _read_segy(filename)

x = np.array(list(raw.textual_file_header.decode()))
print('\n'.join(''.join(row) for row in x.reshape((40, 80))))

data = np.vstack([t.data for t in raw.traces])
print(f"data shape: {data.shape}")

# number of inlines = MAX Line - MIN Line + 1 = 796 - 510 + 1 = 287
inline_number = 287
# number of crosslines = MAX CDP - MIN CDP + 1 = 792 - 58 + 1 = 735
crossline_number = 735
# reshape data to 3D array
data = data.reshape((287, 735, 1252))
print(f"data reshaped to 3D array shape: {data.shape}")

# Tạo lưới ImageData (thay thế cho UniformGrid cũ)
grid = pv.ImageData()

# Thiết lập kích thước lưới
grid.dimensions = np.array(data.shape)

# Thiết lập khoảng cách giữa các điểm (Spacing)
# Bạn có thể điều chỉnh tỉ lệ này để khối địa chấn không bị quá dẹt hoặc quá dài
grid.spacing = (10, 10, 1)  # Giả sử khoảng cách IL, XL là 10m, Time là 1 đơn vị

# Đưa dữ liệu địa chấn vào lưới
grid.point_data["Amplitude"] = data.flatten(order="F")

# Tạo cửa sổ hiển thị
plotter = pv.Plotter(title="SEGY 3D Seismic Visualization (PyVista)")

# CÁCH 1: Hiển thị khối 3D xuyên thấu (Volume Rendering)
# plotter.add_volume(grid, cmap="RdBu", opacity="linear")

# CÁCH 2: Hiển thị các lát cắt (Orthogonal Slices) - Phổ biến nhất trong địa chấn
slices = grid.slice_orthogonal(
    x=grid.dimensions[0]//2, 
    y=grid.dimensions[1]//2, 
    z=grid.dimensions[2]//2
)
plotter.add_mesh(slices, cmap="RdBu", n_colors=256)

# Thêm thanh thước đo và màu sắc
plotter.add_scalar_bar("Amplitude")
plotter.add_axes()
plotter.show_grid()

print("Đang mở cửa sổ hiển thị 3D...")
plotter.show()