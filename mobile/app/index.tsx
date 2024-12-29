import {SafeAreaView, StatusBar, StyleSheet, Text, View} from "react-native";

export default function Index() {
  return (
    <SafeAreaView style = {styles.container}>
        <StatusBar backgroundColor='#E6FFFDFF' barStyle={'dark-content'}/>
      <Text>hello bruh.</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#E6FFFDFF",

    }
})