import { initializeApp } from "firebase/app";
import {getStorage} from "firebase/storage"
const firebaseConfig = {
    apiKey: "AIzaSyA6m1bcIqSs2L3BICyYFdeMvsPYpxG3204",
    authDomain: "theseus-f444c.firebaseapp.com",
    projectId: "theseus-f444c",
    storageBucket: "theseus-f444c.firebasestorage.app",
    messagingSenderId: "313348201458",
    appId: "1:313348201458:web:276560531a3657e80f296b"
};

const app = initializeApp(firebaseConfig);

const storage = getStorage(app);

export {storage}