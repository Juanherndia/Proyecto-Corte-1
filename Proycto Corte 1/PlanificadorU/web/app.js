function mostrar(seccion) {
  ["calendario", "emergencias", "reuniones", "notificaciones"].forEach((id) => {
    document.getElementById(id).className =
      id === seccion ? "visible" : "oculto";
  });
  cargarEventos();
}

function abrirFormulario() {
  document.getElementById("formulario-evento").classList.add("visible");
  document.getElementById("formulario-evento").classList.remove("oculto");
}
function cerrarFormulario() {
  document.getElementById("formulario-evento").classList.remove("visible");
  document.getElementById("formulario-evento").classList.add("oculto");
}

function abrirFormularioEmergencia() {
  document.getElementById("formulario-emergencia").className = "modal visible";
}
function cerrarFormularioEmergencia() {
  document.getElementById("formulario-emergencia").className = "modal oculto";
}

function abrirFormularioReunion() {
  document.getElementById("formulario-reunion").className = "modal visible";
}
function cerrarFormularioReunion() {
  document.getElementById("formulario-reunion").className = "modal oculto";
}

document.getElementById("eventoForm").onsubmit = async function (e) {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(this));
  await fetch("http://localhost:5000/api/evento", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  cerrarFormulario();
  setTimeout(cargarEventos, 200);

  document.getElementById("emergenciaForm").onsubmit = async function (e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(this));
    data.tipo = "emergencia";
    await fetch("http://localhost:5000/api/evento", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    cerrarFormularioEmergencia();
    setTimeout(cargarEventos, 200);
  };

  // Cargar y mostrar eventos guardados
  async function cargarEventos() {
    const res = await fetch("http://localhost:5000/api/eventos");
    const eventos = await res.json();
    // Limpiar listas
    document.getElementById("eventos-lista").innerHTML = "";
    document.getElementById("emergencias-lista").innerHTML = "";
    document.getElementById("reuniones-lista").innerHTML = "";
    // Mostrar eventos según tipo
    eventos.forEach((ev) => {
      if (ev.tipo === "guardia" || ev.tipo === "turno") {
        document.getElementById("eventos-lista").innerHTML += `<li><b>${
          ev.tipo
        }</b>: ${ev.nombre} (${ev.fecha} ${ev.hora}) [${
          ev.especialidad || ""
        }]</li>`;
      } else if (ev.tipo === "emergencia") {
        document.getElementById(
          "emergencias-lista"
        ).innerHTML += `<li><b>Emergencia</b>: ${ev.nombre} (${ev.fecha} ${ev.hora}) - ${ev.descripcion}</li>`;
      } else if (ev.tipo === "reunion") {
        document.getElementById(
          "reuniones-lista"
        ).innerHTML += `<li><b>Reunión</b>: ${ev.nombre} (${ev.fecha} ${ev.hora}) - ${ev.descripcion}</li>`;
      }
    });
  }

  // Cargar eventos al iniciar
  window.onload = cargarEventos;
};

document.getElementById("reunionForm").onsubmit = async function (e) {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(this));
  data.tipo = "reunion";
  await fetch("http://localhost:5000/api/evento", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  cerrarFormularioReunion();
  setTimeout(cargarEventos, 200);
};
