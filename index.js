import axios from "axios";
import fs from "fs";
const lengths = JSON.parse(fs.readFileSync("lengths.json", "utf8"));
var urls = [];
lengths.forEach((l) => {
  for (var x = 0; x < l.chapters; x++) {
    urls.push({
      url: `https://audio.esv.org/david-cochran-heath/mq/${l.book.split(" ").join("+")}+${x + 1}.mp3`,
      name: l.book.split(" ").join("_") + " " + (x + 1),
      filename: `./audio/${l.id.toString().padStart(2, "0")}_${l.book.split(" ").join("_")}-${x + 1}.mp3`,
    });
  }
});

// Atomic counter for tracking download progress
let processedCounter = 0;
const incrementCounter = () => {
  return ++processedCounter;
};

async function download(url, dest, totalCount, index) {
  // Use the passed index for consistent display formatting
  const currentCount = index + 1;

  // Check if file already exists
  if (fs.existsSync(dest)) {
    const count = incrementCounter();
    console.log(
      `Skipping [${currentCount}/${totalCount}] - File already exists (${count} total processed)`,
    );
    return;
  }

  // console.log(`Downloading [${currentCount}/${totalCount}]`);
  const file = fs.createWriteStream(dest);
  const response = await axios.get(url, { responseType: "stream" });
  response.data.pipe(file);

  return new Promise((resolve, reject) => {
    file.on("finish", () => {
      const count = incrementCounter();
      console.log(`Downloaded [${count}/${totalCount}]`);
      resolve();
    });
    file.on("error", (err) => {
      fs.unlink(dest, () => {}); // Delete the file if there was an error
      reject(err);
    });
    response.data.on("error", (err) => {
      fs.unlink(dest, () => {}); // Delete the file if there was an error
      reject(err);
    });
  });
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

(async () => {
  console.log("Starting");
  const totalCount = urls.length;
  const batchSize = 10;
  var wait = true;

  // Create audio directory if it doesn't exist
  if (!fs.existsSync("./audio")) {
    fs.mkdirSync("./audio", { recursive: true });
  }

  for (let i = 0; i < urls.length; i += batchSize) {
    const batch = urls.slice(i, i + batchSize);

    wait = batch.map((item) => fs.existsSync(item.filename)).includes(false);

    const promises = batch.map((url, batchIndex) =>
      download(url.url, url.filename, totalCount, i + batchIndex),
    );
    await Promise.all(promises);

    if (i + batchSize < urls.length && wait) {
      console.log("Waiting 100ms before next batch...");
      await sleep(100);
      wait = true;
    }
  }

  console.log("Done");
})();
