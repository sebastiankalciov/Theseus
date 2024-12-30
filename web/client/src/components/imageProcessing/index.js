import axios from 'axios';

export const handleImageProcess = async (imageURL) => {
    try {
        console.log(imageURL);
        const response = await axios.post('http://localhost:5000/process-image', {imageURL:imageURL});
        console.log("response from py code execution: ", response);
    } catch (e) {
        console.error("error when handling image processing: ", e);
    }
}