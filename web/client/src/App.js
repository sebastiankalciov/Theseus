import './App.css';
import {storage} from "./firebase/config";
import {ref, getDownloadURL} from "firebase/storage";
import {useEffect, useState} from "react";

function App() {
    const [imageURL, setImageURL] = useState(null);

    const fetchImage = async () => {
        try {
            const referenceToImage = ref(storage,  'unprocessed-images/image.jpg');
            const url = await getDownloadURL(referenceToImage);
            setImageURL(url);
        } catch (e) {
            console.error("error when fetching image from firebase: ", e);
        }
    }

    useEffect(() => {
        // get image from the firebase
        fetchImage();
    })

    return (
    <div className="App">
        <header className="App-header">
            <h1 id="image-container-title">Last image</h1>

            <div className="card">
                <div className="card-overlay"></div>
                <div className="card-inner">
                    {imageURL ? (
                        <img src={imageURL} alt="fetched from firebase" style={{width: "250px", height: "400px"}}/>
                    ) : (
                        <p>Loading image...</p>
                    )}
                </div>
            </div>

            <button>Process image</button>
        </header>
    </div>
    );
}

export default App;
