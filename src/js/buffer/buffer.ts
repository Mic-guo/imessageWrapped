import { TypedStreamReader, Unarchiver } from "../utils_ts";
import { BPlistReader } from "../utils_ts/bplist";

export const decodeMessageBuffer = async (buffer: Buffer | Uint8Array | undefined) => {
  console.log("IN BUFFER")
  console.log(buffer)
  try {
    console.log("Before uint8array check")
    if (buffer instanceof Uint8Array) {
      console.log("INSIDE uint8array check")
      try {
        buffer = Buffer.from(buffer);
      }
      catch (e) {
        console.error("Error in decodeMessageBuffer:", e);
      }
    }
    console.log("After uint8array check")
    if (buffer instanceof Buffer && buffer.length) {
      if (buffer.subarray(0, 6).toString() === "bplist") {
        const reader = new BPlistReader(buffer);
        const parsed = reader.read();
        console.log(`${parsed}`)
        return parsed;
      }

      const read = new TypedStreamReader(buffer);
      const unarchiver = new Unarchiver(read);
      console.log(`Decoded String ${unarchiver}`)
      return unarchiver.decodeAll();
    }
  } catch (e) {
    // ignore
  }
  return buffer;
};

export const getTextFromBuffer = async (buffer: Buffer | Uint8Array | undefined) => {
  try {
    const parsed = await decodeMessageBuffer(buffer);
    if (parsed) {
      const string = parsed[0]?.value?.string;
      if (string) {
        return (string || "").trim().replace(/[\u{FFFC}-\u{FFFD}]/gu, "");
      }
    }
  } catch {
    //skip
  }

  return null;
};