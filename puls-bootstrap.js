if ("serviceWorker" in navigator && location.protocol !== "file:") {
  navigator.serviceWorker.register("./service-worker.js").catch((error) => {
    console.warn("Modul offline PULS nu a putut fi activat.", error);
  });
}
