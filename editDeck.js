//This is messy as hell. In short, I wrote this to add the stroke order png's to each card in my kanji deck.

const fs = require('fs')

// Read the image file
async function ReadImgFile (location) {
  try {
    const data = fs.readFileSync(location);
    return Buffer.from(data).toString('base64');
  } catch (err) {
    console.error(err);
    return null;
  }
};
async function CharToUnicode(char) {
  return hexString = char.charCodeAt(0).toString(16);
}

async function invoke (action, version, params = {}) {
  return new Promise((resolve, reject) => {
    const response = fetch('http://127.0.0.1:8765', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ action, version, params })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then(data => {
        if (Object.getOwnPropertyNames(data).length != 2) {
          throw new Error('Response has an unexpected number of fields')
        }
        if (!data.hasOwnProperty('error')) {
          throw new Error('Response is missing required error field')
        }
        if (!data.hasOwnProperty('result')) {
          throw new Error('Response is missing required result field')
        }
        if (data.error) {
          throw new Error(data.error)
        }
        resolve(data.result)
      })
      .catch(error => {
        reject(error)
      })
  })
}

async function action () {
  let count = 0;
  let failCount = 0;
  const uniqueCard = [];
  const seen = new Set();

  let answer = await invoke('findCards', 6, { query: 'deck:"RTK order Kanji"' })
  let cardInfo = await invoke('cardsInfo', 6, { cards: answer })

  for (const note of cardInfo) {
    if (!seen.has(note.note)) {
      uniqueCard.push(note);
      seen.add(note.note);
    }
  }
  for (const card of uniqueCard) {
    let cardId = card.note;
    let hexString = await CharToUnicode(card.fields.Kanji.value);
    let img64 = await ReadImgFile(`./KanjiStrokeOrder/${hexString}.png`);

    if (img64) {
      count++
      await invoke('storeMediaFile', 6, {
        filename: `${hexString}.png`,
        data: img64
      })
      await invoke('updateNoteFields', 6, {
        note: {
          id: cardId,
          fields: {
            'Stroke Order': `<img src=${hexString}.png>`
          }
        }
      })
      console.log(card.fields["Stroke Order"]);
    } else {
      failCount++;
    }
  };

  console.log(`Edit complete. ${count} fields were changed and ${failCount} kanji were not found.`)
}

action()
