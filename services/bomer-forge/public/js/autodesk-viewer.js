/**
 * Generates access token for viewing models in the Model Derivative service.
 * @param {(string, number) => void} callback Function that will be called with generated access token and number of seconds before it expires.
 */
export function getAccessToken(callback) {
  callback(
    "eyJhbGciOiJSUzI1NiIsImtpZCI6ImI4YjJkMzNhLTFlOTYtNDYwNS1iMWE4LTgwYjRhNWE4YjNlNyIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2F1dG9kZXNrLmNvbSIsImNsaWVudF9pZCI6InE4MW9SRlh2VGFtVkdEeXdocVRSZnB1cmFMSVlBRkprQklvekpob0xjVGx0S2FtZyIsInNjb3BlIjpbImRhdGE6cmVhZCIsImRhdGE6d3JpdGUiLCJkYXRhOmNyZWF0ZSIsImJ1Y2tldDpjcmVhdGUiLCJidWNrZXQ6cmVhZCJdLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiZXhwIjoxNzQyODE4NjMzLCJqdGkiOiJBVC1iY2ZiMzhiZC0xMTQ5LTQ1ZjMtOGFlMi0wY2RlZGNjNDBhY2YifQ.gL1p3Rof8GldyUmb6DPVqwfRSKAO1EYG7NeUDEMOUNXgEzOBffTDJ6xWKntmBMvdNfDeoTkPgr-60E-W28W8hzqGkIMl8vdSPfXLoRbTu-gv_yfUwrfQJTnuSfwPyYOTAeWwdMFSSQqsic-6CsoQwRo_n9xLZAjQUBlMCGF0HLfEQJMGebGDDB-8R4jt2khJrlW7BGL-SC_JkgW5YBrRGaFxcAIzFhqokGn8CiODBWH4uhk7TcwPkCjirwK8NOiZkfM_b0eni7hPYz9I-OeiSbRsCUCmreGfCBMmF3MCjM9cBjRxEaJfuHzdAWhvsqmz7MKmIfwr3B_6YLtgfzw3NA",
    3599
  );
  // fetch(APP_URL + "/api/token")
  //   .then((resp) => (resp.ok ? resp.json() : Promise.reject(resp)))
  //   .then((credentials) =>
  //     callback(credentials.access_token, credentials.expires_in)
  //   )
  //   .catch((err) => {
  //     console.error(err);
  //     alert("Could not get access token. See console for more details.");
  //   });
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
    Autodesk.Viewing.Initializer({ getAccessToken }, function () {
      const viewer = new Autodesk.Viewing.GuiViewer3D(container, config);
      viewer.start();
      resolve(viewer);
    });
  });
}

/**
 * Loads specific model into the viewer.
 * @param {Autodesk.Viewing.GuiViewer3D} viewer Target viewer.
 * @param {string} urn URN of the model in the Model Derivative service.
 */
export function loadModel(viewer, urn) {
  Autodesk.Viewing.Document.load(
    "urn:" + urn,
    (doc) => {
      // Get all 2D viewables
      const viewables = doc.getRoot().search({ type: "geometry", role: "2d" });

      // Look for the specific "2D View" viewable
      let modelViewable = null;
      for (let i = 0; i < viewables.length; i++) {
        if (viewables[i].name() === "2D View") {
          modelViewable = viewables[i];
          break;
        }
      }

      // If found, load the 2D View
      if (modelViewable) {
        viewer.loadDocumentNode(doc, modelViewable);
        console.log("Loaded 2D View:", modelViewable.name());
      } else {
        // Fall back to default behavior if no 2D View found
        viewer.loadDocumentNode(doc, doc.getRoot().getDefaultGeometry());
        console.log("No 2D View found, loaded default geometry");
      }
    },
    (code, message, errors) => {
      console.error(code, message, errors);
      alert("Could not load model. See console for more details.");
    }
  );
}

function crop(viewer, w, h) {
  let vw = viewer.container.clientWidth;
  let vh = viewer.container.clientHeight;

  if (w > vw || h > vh) {
    alert("Dimensions should not be larger than Viewer");
    return;
  }

  viewer.getScreenShot(vw, vh, (blob) => {
    var canvas = document.getElementById("MyCanvas");
    var ctx = canvas.getContext("2d");
    canvas.width = w;
    canvas.height = h;
    var image = new Image();
    image.onload = () => {
      ctx.clearRect(0, 0, w, h);
      let sx = (vw - w) / 2;
      let sy = (vh - h) / 2;
      ctx.drawImage(image, sx, sy, w, h, 0, 0, w, h);
    };
    image.src = blob;
  });
}

async function init() {
  const viewer = await initViewer(document.getElementById("forgeViewer"), {
    extendStringsFetching: true,
    thickness: 0.05,
  });
  console.log(viewer);
  loadModel(
    viewer,
    // "adsk.objects:os.object:beaver-blueprints-bucket/structure-drawing.dwg"
    "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6YmVhdmVyLWJsdWVwcmludHMtYnVja2V0L3N0cnVjdHVyZS1kcmF3aW5nLmR3Zw"
  );
}

await init();
