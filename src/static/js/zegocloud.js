(async () => {
    const appID = 376109737; // Reemplaza con tu AppID de ZEGOCLOUD
    const serverSecret = "621e0900146418c8d7f7c790e3c79cc4"; // Reemplaza con tu ServerSecret

    const urlParams = new URLSearchParams(window.location.search);
    const roomID = urlParams.get("roomID") || "defaultRoom";

    const userID = `user_${Math.floor(Math.random() * 10000)}`;
    const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(
        appID,
        serverSecret,
        roomID,
        userID,
        `User-${userID}`
    );

    const zp = ZegoUIKitPrebuilt.create(kitToken);
    zp.joinRoom({
        container: document.getElementById("video-call"),
        scenario: {
            mode: ZegoUIKitPrebuilt.VideoConference,
        },
    });
})();
