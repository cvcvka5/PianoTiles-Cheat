import streamlit as st
from version import VERSION
from utils.pianotiles import select_game_border_points, get_frame, start_cheat, marked_spots
import dxcam


st.session_state.setdefault("game_border_xys", None)
st.session_state.setdefault("game_area_screenshot", None)
st.session_state.setdefault("dxcam", None)

    



st.title(f"🎹PianoTiles Cheat {VERSION}")


st.button("ℹ️Determine game boundary", help="You must choose the top-left then the bottom-right of the game area.",
          on_click=lambda: st.session_state.__setitem__("game_border_xys", select_game_border_points()),
          disabled=st.session_state.get("game_border_xys") is not None)

xy1, xy2 = st.columns(2)

if (st.session_state.get("game_border_xys") is not None) and (st.session_state.get("game_area_screenshot") is None):
    camera = dxcam.create(output_idx=0, output_color="BGR")
    borders_xy = st.session_state.get("game_border_xys")
    st.session_state.dxcam = camera
    st.session_state.game_area_screenshot = marked_spots(get_frame(st.session_state.get("dxcam"), st.session_state.get("game_border_xys")))

    xy1.text(st.session_state.get("game_border_xys")[0])
    xy2.text(st.session_state.get("game_border_xys")[1])
try:
    st.image(st.session_state.get("game_area_screenshot"), channels="BGR")
except AttributeError:
    pass

st.button("🚀 Start cheat", on_click=lambda: start_cheat(st.session_state.dxcam, st.session_state.get("game_border_xys")),
          disabled=(st.session_state.get("game_border_xys") is None) or (st.session_state.get("game_area_screenshot") is None))


