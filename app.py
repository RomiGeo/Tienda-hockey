
import streamlit as st
import json
import os

ARCHIVO = "productos.json"

def cargar_productos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_productos(productos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

st.set_page_config(page_title="Tienda de Hockey", page_icon="🏑", layout="wide")

st.markdown(
    '''
    <style>
    body {
        background-color: #eaf4fc;
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
    }
    h1 {
        color: #004080;
    }
    .producto {
        border: 2px solid #004080;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
        background-color: #f0f8ff;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

if "productos" not in st.session_state:
    st.session_state.productos = cargar_productos()

if "carrito" not in st.session_state:
    st.session_state.carrito = []

st.image("https://img.icons8.com/color/96/hockey.png", width=80)
st.title("🏑 Tienda Virtual de Hockey 🎽")
st.write("Agregá productos a tu tienda de juego y jugá a comprar en el carrito.")

with st.expander("➕ Agregar nuevo producto"):
    with st.form("form_producto"):
        nombre = st.text_input("Nombre del producto")
        precio = st.number_input("Precio ($)", min_value=0.0, format="%.2f")
        detalle = st.text_area("Detalles")
        imagen = st.text_input("URL de la imagen (ej: https://...)")
        agregar = st.form_submit_button("Agregar producto")

        if agregar and nombre:
            st.session_state.productos.append({
                "nombre": nombre,
                "precio": precio,
                "detalle": detalle,
                "imagen": imagen
            })
            guardar_productos(st.session_state.productos)
            st.success(f"✅ {nombre} agregado a la tienda!")

st.subheader("🛍️ Productos en la tienda")

for i, p in enumerate(st.session_state.productos):
    with st.container():
        st.markdown(f"<div class='producto'>", unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            if p["imagen"]:
                st.image(p["imagen"], width=120)
        with cols[1]:
            st.write(f"### {p['nombre']}")
            st.write(f"💲 **${p['precio']}**")
            st.write(p["detalle"])
            if st.button(f"🛒 Agregar al carrito", key=f"btn{i}"):
                st.session_state.carrito.append(p)
                st.success(f"{p['nombre']} agregado al carrito!")
        st.markdown("</div>", unsafe_allow_html=True)

st.subheader("🛒 Carrito de compras (ficticio)")

if st.session_state.carrito:
    total = 0
    for item in st.session_state.carrito:
        st.write(f"- {item['nombre']} (${item['precio']})")
        total += item["precio"]
    st.write(f"### 💰 Total: ${total:.2f}")
else:
    st.info("Tu carrito está vacío. Agregá productos para jugar.")
