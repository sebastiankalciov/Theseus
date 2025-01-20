import axios from 'axios';

export const handleImageProcess = async (imageURL) => {
    try {
        console.log(imageURL);

        // send a request to process the image from the url 'imageURL'
        // then return as a response the graph in a json format
        const response = await axios.post('http://localhost:5000/process-image', {imageURL:imageURL});
        console.log("response from py code execution: ", response);
        return response.data.body ? JSON.parse(response.data.body) : null;
    } catch (e) {
        console.error("error when handling image processing: ", e);
    }
}