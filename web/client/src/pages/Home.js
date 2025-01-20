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
            <header className="App-header" style = {{flexDirection: 'row', display: 'flex'}}>
                <div style = {{marginRight: '10%', }}>
                    <h1 id="image-container-title">Instructions</h1>
                    <ul style = {{listStyleType: 'none', color: '#253434', fontSize: '30px'}}>
                        <li><b>Draw a simple polygon </b>
                        </li>
                        <li>
                            The polygon must have clear lines, with <b style = {{color: "#e95847"}}>NO</b> interruption<br/>
                            It must have a margin of at least <b>6cm</b><br/>
                            It must <b style = {{color: "#e95847"}}>NOT</b> be extremely complicated <br/>
                            (it might fail when building the graph from the processed image)
                        </li>
                        <br/>
                        <li><b>Draw start & finish points</b></li>
                        <li>The points must be a bit large (around <b>1cm</b>)</li>
                        <br/>
                        <li><b>Click "Process image" button and wait</b></li>
                        <li>It takes around <b>5s</b> to process the image and animate it on the screen</li>
                    </ul>
                </div>
                <div>
                <h1 id="image-container-title">Last image</h1>

                <div className="card">
                    <div className="card-overlay"></div>
                    <div className="card-inner">
                        {imageURL ? (
                            <img src={imageURL} alt="fetched from firebase" style={{width: "650px", height: "400px"}}/>
                        ) : (
                            <p>Loading image...</p>
                        )}
                    </div>
                </div>

                <button onClick={handleImageProcessing}>Process image</button>
                </div>
            </header>
        </div>
    )
}

export default Home;