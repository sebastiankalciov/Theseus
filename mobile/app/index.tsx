import {Alert, Button, Pressable, SafeAreaView, StatusBar, StyleSheet, Text, View} from "react-native";
import {useRef, useState} from "react";
import {CameraType, CameraView, useCameraPermissions} from "expo-camera";
import {FontAwesome5} from "@expo/vector-icons";

import {uploadImage} from "@/utils/uploadImage";

export default function Index() {
    const [facing] = useState<CameraType>('back');
    const [permission, requestPermission] = useCameraPermissions();
    const cameraReference = useRef<CameraView>(null);
    const [picture, setPicture] = useState<string>("");

    if (!permission) {
        return <View />;
    }

    if (!permission.granted) {
        return (
            <View>
                <Text>We need your permission to show the camera</Text>
                <Button onPress={requestPermission} title="grant permission" />
            </View>
        );
    }

    const sendImage = async () => {

        if (!cameraReference) {
            console.error("error when capturing picture");
            return;
        }

        try {
            const capturedImage = await cameraReference.current?.takePictureAsync();

            if (!capturedImage?.uri) {
                Alert.alert("Image", "Failed to capture the image. Please try again.");
                return;
            }

            setPicture(capturedImage!.uri);
            const imageURL = await uploadImage(capturedImage!.uri);
            if (imageURL === null) {
                Alert.alert("Upload image", "Failed to upload the image. Please try again.");
                return;
            }

            Alert.alert("Upload image", "Image uploaded successfully!");
            console.log(imageURL);
        } catch (error) {
            console.log("error when uploading image: ", error);
            return;
        }
    }

    return (
        <SafeAreaView style = {styles.container}>
            <StatusBar backgroundColor='#E6FFFDFF' barStyle={'dark-content'}/>
            <CameraView style={styles.camera} facing={facing} ref = {cameraReference}>
                <View style = {styles.buttonContainer}>
                    <Pressable style = {styles.capturePictureButton} onPress = {sendImage}>
                        <FontAwesome5 name = "circle" size = {70} color = "#fff"/>
                    </Pressable>
                </View>
            </CameraView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#E6FFFDFF",

    },
    camera: {
        flex: 1,
        paddingBottom: 20
    },
    buttonContainer: {
        flex: 1,
        justifyContent: "flex-end",
        backgroundColor: 'transparent',

    },
    icon: {
        position: "absolute",
        color: "#c6c6c6"
    },
    capturePictureButton: {
        alignItems: "center",
        justifyContent: "center",
    },
})