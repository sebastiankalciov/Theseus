import {getDownloadURL, ref, uploadBytes} from "@firebase/storage";
import {storage} from "@/firebase/config";
import {Alert} from "react-native";

export const uploadImage = async (picture: string) => {
    try {
        const response = await fetch(picture);
        const blob = await response.blob();
        const date = new Date();

        //const formattedDate = date.toLocaleString().split(", ").join("--").replaceAll(".", "-")

        const referenceToImage = ref(storage, `unprocessed-images/image.jpg`);

        const result  = await uploadBytes(referenceToImage, blob);
        const url = await getDownloadURL(result.ref);

        return url;
    } catch (e) {
        console.error("error when sending image: ", e);
        return null;
    }
}