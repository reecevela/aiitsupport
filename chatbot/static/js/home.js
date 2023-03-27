$(document).ready(function () {
    const examples = [
        "adding a printer",
        "troubleshooting network issues",
        "custom applications",
        "fixing Wi-Fi connectivity",
        "installing software and updates",
        "fixing printer connections",
        "recovering lost or deleted files",
        "configuring display settings",
        "fixing audio and video issues",
        "managing browser extensions",
        "setting up a VPN connection",
        "addressing USB device problems",
        "configuring mobile hotspot",
        "identifying suspicious emails",
        "configuring privacy settings",
    ];
    let exampleIndex = 0;

    function changeExample() {
        $("#example-text")
            .animate({ opacity: 0, marginTop: "-20px" }, 500, function () {
                exampleIndex = (exampleIndex + 1) % examples.length;
                $(this)
                    .text(examples[exampleIndex])
                    .css("marginTop", "20px")
                    .animate({ opacity: 1, marginTop: "0px" }, 500);
            });
    }

    setInterval(changeExample, 4000); // Change the time here to control the speed of the text change
});


