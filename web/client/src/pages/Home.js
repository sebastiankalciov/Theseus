import '../styles/App.css';
import {useEffect, useState} from "react";
import {getDownloadURL, ref} from "firebase/storage";
import {storage} from "../firebase/config";
import {useNavigate} from "react-router-dom";
import {handleImageProcess} from "../components/imageProcessing";

function Home() {
    const [imageURL, setImageURL] = useState(null);
    const [processedData, setProcessedData] = useState(null);

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
    }, []);

    const navigate = useNavigate();

    const handleImageProcessing = async () => {
        const data = await handleImageProcess(imageURL);
        setProcessedData(data)
        navigate('./AnimationPage', { state: { data: data } });
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1 id="image-container-title">Last image</h1>

                <div className="card">
                    <div className="card-overlay"></div>
                    <div className="card-inner">
                        {imageURL ? (
                            <img src={imageURL} alt="fetched from firebase" style={{width: "450px", height: "400px"}}/>
                        ) : (
                            <p>Loading image...</p>
                        )}
                    </div>
                </div>

                <button onClick={handleImageProcessing}>Process image</button>
            </header>
        </div>
    )
}

export default Home;