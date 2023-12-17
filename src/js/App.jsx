import React, { useState, useEffect } from "react";
import "./css/index.css";
// import * as SQL from 'sql.js';
import initSqlJs from "sql.js";
import { decodeMessageBuffer, getTextFromBuffer } from "./buffer/buffer";
import AtRule from "postcss/lib/at-rule";
// import sqlWasm from "!!file-loader?name=sql-wasm-[contenthash].wasm!sql.js/dist/sql-wasm.wasm";

async function updateMessages(db) {
  const messagesWithNullText = await db.exec(`
                          SELECT attributedBody 
                          FROM message
                          WHERE text IS NULL AND attributedBody IS NOT NULL
                          LIMIT 15;
                        `);
  console.log(messagesWithNullText[0]);
  if (messagesWithNullText.length) {
    // console.log(
    //   `Adding parsed text to ${messagesWithNullText.length} messages`
    // );
    const firstQueryResult = messagesWithNullText[0];
    for (const attributedBody of firstQueryResult.values) {
      // const attributedBody = row[0]; // Since there's only one column, it's the first element
      console.log(attributedBody[0]);
      const parsed = await decodeMessageBuffer(attributedBody[0]);
      if (parsed) {
        const string = parsed[0]?.value?.string;
        if (typeof string === "string") {
          console.log(string);
        }
      }
      // Now you can work with each 'attributedBody' value
      // console.log(attributedBody);
    }

    // await db.transaction().execute(async (trx) => {
    // for (const message of messagesWithNullText.value) {
    //   try {
    //     const { attributedBody, ROWID } = message;
    //     if (attributedBody) {
    //       const parsed = await decodeMessageBuffer(attributedBody);
    //       if (parsed) {
    //         const string = parsed[0]?.value?.string;
    //         console.log(string);
    //         // Update the database with the new string
    //         // Add your database update logic here
    //       }
    //     }
    //   } catch (error) {
    //     console.error("Error updating message:", error);
    //   }
    // }
    // });
  }
}

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [db, setDb] = useState(null);

  useEffect(() => {
    const fileSelector = document.getElementById("file-selector");
    fileSelector.addEventListener("change", handleFileChange);

    // Cleanup event listener when component unmounts
    return () => {
      fileSelector.removeEventListener("change", handleFileChange);
    };
  }, [selectedFile]); // Empty dependency array ensures that the effect runs only once after initial render

  const handleFileChange = (event) => {
    const files = event.target.files;
    const reader = new FileReader();

    if (files.length > 0) {
      reader.addEventListener("load", async (event) => {
        try {
          const result = event.target.result;
          // console.log(result)
          // Convert the ArrayBuffer to a Uint8Array
          const uint8Array = new Uint8Array(result);
          // console.log(uint8Array)

          try {
            // Assuming you have a Uint8Array named database Data containing SQLite database content
            const databaseData = uint8Array;

            // Initialize the database using the provided Uint8Array
            const SQL = await initSqlJs({
              locateFile: (file) => {
                if (file.endsWith(".wasm")) {
                  return "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.9.0/sql-wasm.wasm";
                }
                return `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.9.0/${file}`;
              },
            });
            const db = new SQL.Database(databaseData);
            await updateMessages(db);

            // const queryResult = db.exec(`
            //                         SELECT date, id, text
            //                         FROM message
            //                         LEFT JOIN handle ON message.handle_id = handle.ROWID
            //                         ORDER BY date DESC
            //                       `);

            // // Fetch results
            // if (queryResult.length > 0 && queryResult[0].values) {
            //   const resultSet = queryResult[0].values;
            //   console.log("Query Result Set:", resultSet);
            // } else {
            //   console.error("No results returned from the query.");
            // }
            setDb(db);
          } catch (err) {
            console.log(err);
          }
        } catch (error) {
          console.error("Error reading or querying the database:", error);
        }
      });

      reader.addEventListener("progress", (event) => {
        if (event.loaded && event.total) {
          const percent = (event.loaded / event.total) * 100;
          console.log(`Progress: ${Math.round(percent)}`);
        }
      });

      // Read the file as an ArrayBuffer (binary data)
      reader.readAsArrayBuffer(files[0]);

      setSelectedFile(files[0]);
    }
  };

  const clearFileSelection = () => {
    setSelectedFile(null);
    const fileSelector = document.getElementById("file-selector");
    if (fileSelector) {
      fileSelector.value = ""; // Clear the file input
    }
    console.clear();
  };

  return (
    <>
      <div className="font-mukta-malar flex flex-col h-screen justify-center items-center bg-pink-200 text-white">
        <div>
          <p className="font-sans text-5xl">Attach your chat.db</p>
        </div>
        <div className="flex flex-col">
          <input type="file" id="file-selector" />
          {/* {selectedFile && (
            <div>
              <h3>Selected File:</h3>
              <p>{selectedFile.name}</p>
            </div>
          )} */}
          <button className=" p-2 shadow-lg w-28" onClick={clearFileSelection}>
            Clear File
          </button>
        </div>

        {/* {selectedFile && (
          <getInfoButton
          
          />
        )} */}
      </div>
    </>
  );
}

function getInfoButton({ file }) {
  const toggleInfo = () => {
    const secondLikeUrl = `/api/v1/likes/?postid=${postId}`;
    fetch(secondLikeUrl, {
      method: "POST",
      // body: JSON.stringify({ postid: postId }),
      // headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setLognameLikes(true);
        setNumLikes(numLikes + 1);
        setLikeUrl(data.url);
      })
      .catch((error) => console.log(error));
  };

  return initialIsLiked !== undefined ? (
    <button type="button" onClick={toggleInfo}>
      {initialIsLiked ? "Unlike" : "Like"}
    </button>
  ) : null;
}

export default App;
