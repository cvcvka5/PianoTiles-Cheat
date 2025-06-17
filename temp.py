import dxcam
import cv2 as cv

def get_dxcam() -> dxcam.DXCamera:
    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=240)
    return camera

frame = get_dxcam().get_latest_frame()
print(type(frame))
cv.imshow("frm", frame)
cv.waitKey(0)