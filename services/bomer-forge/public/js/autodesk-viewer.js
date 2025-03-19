import ModelJson from "./model.json";
/**
 * Generates access token for viewing models in the Model Derivative service.
 * @param {(string, number) => void} callback Function that will be called with generated access token and number of seconds before it expires.
 */
export function getAccessToken(callback) {
  fetch(APP_URL + "/api/token")
    .then((resp) => (resp.ok ? resp.json() : Promise.reject(resp)))
    .then((credentials) =>
      callback(credentials.access_token, credentials.expires_in)
    )
    .catch((err) => {
      console.error(err);
      alert("Could not get access token. See console for more details.");
    });
}

/**
 * Initializes the runtime for communicating with the Model Derivative service, and creates a new instance of viewer.
 * @async
 * @param {HTMLElement} container Container that will host the viewer.
 * @param {object} config Additional configuration options for the new viewer instance.
 * @returns {Promise<Autodesk.Viewing.GuiViewer3D>} New viewer instance.
 */
export function initViewer(container, config) {
  return new Promise(function (resolve) {
    // Autodesk.Viewing.Initializer({ getAccessToken }, function () {
    //   const viewer = new Autodesk.Viewing.GuiViewer3D(container, config);
    //   viewer.start();
    //   resolve(viewer);
    // });
    const viewer = new Autodesk.Viewing.GuiViewer3D(container, config);
    viewer.start();
    resolve(viewer);
  });
}

/**
 * Lists all models available for viewing.
 * @async
 * @returns {Promise<{ name: string, urn: string }>} List of models.
 */
export function listModels() {
  return fetch(APP_URL + "/api/models").then((resp) =>
    resp.ok ? resp.json() : Promise.reject(resp)
  );
}

/**
 * Loads specific model into the viewer.
 * @param {Autodesk.Viewing.GuiViewer3D} viewer Target viewer.
 * @param {string} urn URN of the model in the Model Derivative service.
 */
export function loadModel(viewer, urn) {
  Autodesk.Viewing.Document.load(
    "urn:" + urn,
    (doc) => viewer.loadDocumentNode(doc, doc.getRoot().getDefaultGeometry()),
    (code, message, errors) => {
      console.error(code, message, errors);
      alert("Could not load model. See console for more details.");
    }
  );
}

async function init() {
  const viewer = await initViewer(document.getElementById("viewer"));
  // const models = await listModels();
  // const dropdown = document.getElementById("models");
  // dropdown.innerHTML = models
  //   .map((m) => `<option value="${m.urn}">${m.name}</option>`)
  //   .join("");
  // dropdown.onchange = () => dropdown.value && loadModel(viewer, dropdown.value);
  // dropdown.onchange();
  console.log(
    "adsk.objects:os.object:beaver-blueprints-bucket/structure-drawing.dwg"
  );
  loadModel(
    viewer,
    "adsk.objects:os.object:beaver-blueprints-bucket/structure-drawing.dwg"
  );
  document.getElementById("explode").addEventListener("click", function () {
    if (viewer.getExplodeScale() > 0.0) {
      viewer.explode(0.0);
    } else {
      viewer.explode(0.5);
    }
  });
}

console.log("• Autodesk Viewer initializing");
await init();
console.log("• Autodesk Viewer initialized");
