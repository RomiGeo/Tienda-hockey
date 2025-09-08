import streamlit as st
import json
import os

# ---------------------------
# Funciones auxiliares
# ---------------------------
ARCHIVO = "productos.json"

def cargar_productos():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def guardar_productos(productos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

# ---------------------------
# Configuración de página
# ---------------------------
st.set_page_config(page_title="Hockey Stick-in", page_icon="🏑", layout="wide")

# Estilos
st.markdown(
    """
    <style>
    body {background-color: #eaf4fc;}
    .main {background-color: #ffffff; border-radius: 15px; padding: 20px;}
    h1 {color: #004080;}
    .producto {border: 2px solid #004080; border-radius: 10px; padding: 10px; margin-bottom: 15px; background-color: #f0f8ff;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Estado de la app
# ---------------------------
if "productos" not in st.session_state:
    st.session_state.productos = cargar_productos()

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "editar_index" not in st.session_state:
    st.session_state.editar_index = None

# ---------------------------
# Cabecera con imagen centrada y más pequeña
# ---------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:12px;">
        <img src="imagenes/palo.png" style="width:100px; height:auto; margin-bottom:8px;">
        <h1 style="color:#004080; margin:0;">Hockey Stick-in</h1>
        <p style="color:#666666; margin:0;">Elegí productos y agregá al carrito</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Formulario para agregar / editar productos
# ---------------------------
with st.expander("➕ Agregar o editar producto"):
    with st.form("form_producto"):
        nombre = st.text_input("Nombre del producto")
        precio = st.number_input("Precio ($)", min_value=0.0, format="%.2f")
        detalle = st.text_area("Detalles")
        imagen_archivo = st.file_uploader("Subí una imagen del producto", type=["png", "jpg", "jpeg"])

        if st.session_state.editar_index is not None:
            st.form_submit_button("Guardar cambios")
        agregar = st.form_submit_button("Agregar producto" if st.session_state.editar_index is None else "Guardar cambios")

        if agregar and nombre:
            imagen_path = ""
            if imagen_archivo is not None:
                carpeta_imagenes = "imagenes"
                if not os.path.exists(carpeta_imagenes):
                    os.makedirs(carpeta_imagenes)
                imagen_path = os.path.join(carpeta_imagenes, imagen_archivo.name)
                with open(imagen_path, "wb") as f:
                    f.write(imagen_archivo.getbuffer())

            producto_nuevo = {
                "nombre": nombre,
                "precio": precio,
                "detalle": detalle,
                "imagen": imagen_path
            }

            if st.session_state.editar_index is not None:
                index = st.session_state.editar_index
                if not imagen_path:
                    producto_nuevo["imagen"] = st.session_state.productos[index]["imagen"]
                st.session_state.productos[index] = producto_nuevo
                st.success(f"✏️ {nombre} modificado correctamente!")
                st.session_state.editar_index = None
            else:
                st.session_state.productos.append(producto_nuevo)
                st.success(f"✅ {nombre} agregado a la tienda!")

            guardar_productos(st.session_state.productos)

# ---------------------------
# Mostrar productos
# ---------------------------
st.subheader("🛍️ Productos en la tienda")

for i, p in enumerate(st.session_state.productos):
    with st.container():
        st.markdown(f"<div class='producto'>", unsafe_allow_html=True)
        cols = st.columns([1, 4, 1])
        with cols[0]:
            if p["imagen"]:
                st.image(p["imagen"], width=120)
        with cols[1]:
            st.write(f"### {p['nombre']}")
            st.write(f"💲 **${p['precio']}**")
            st.write(p["detalle"])
        with cols[2]:
            if st.button(f"🛒 Agregar al carrito", key=f"btn_carrito_{i}"):
                st.session_state.carrito.append(p)
                st.success(f"{p['nombre']} agregado al carrito!")
            if st.button(f"✏️ Editar", key=f"btn_editar_{i}"):
                st.session_state.editar_index = i
                st.experimental_rerun()
            if st.button(f"❌ Eliminar", key=f"btn_eliminar_{i}"):
                st.session_state.productos.pop(i)
                guardar_productos(st.session_state.productos)
                st.success(f"{p['nombre']} eliminado de la tienda!")
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Carrito de compras
# ---------------------------
st.subheader("🛒 Carrito de compras (ficticio)")

if st.session_state.carrito:
    total = 0
    for idx, item in enumerate(st.session_state.carrito):
        cols = st.columns([4, 1])
        with cols[0]:
            st.write(f"- {item['nombre']} (${item['precio']})")
        with cols[1]:
            if st.button(f"❌ Quitar", key=f"carrito_quitar_{idx}"):
                st.session_state.carrito.pop(idx)
                st.experimental_rerun()
        total += item["precio"]
    st.write(f"### 💰 Total: ${total:.2f}")
else:
    st.info("Tu carrito está vacío. Agregá productos para jugar.")
