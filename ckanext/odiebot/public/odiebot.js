//
// Call the function below to embed odiebot
// e.g.
//    <script src="/odiebot.js" defer onload="odiebot('...')"/></script>
//
function odiebot(initial_token) {
  var botScript = document.createElement("script");
  botScript.src =
    "https://cdn.botframework.com/botframework-webchat/master/webchat.js";

  botScript.onload = function () {
    load_bot();
    init_bot(initial_token)
      .then(() => console.log("odiebot init OK"))
      .catch((error) => console.error("odiebot init failed", error));
  };
  document.body.appendChild(botScript);
}

function load_bot() {
  const botDiv = document.createElement("div");
  botDiv.id = "webchat";
  botDiv.innerHTML = `
	<div id="va" class="virtual-assistant-wrap" style="height: 0px;" aria-hidden="true">
		<div class="va-wrap-out">
			<div class="va-wrap-in">
				<div class="va-header-wrap">
					<div class="va-header">
						<h1>Odie Bot</h1>
						<a href="javascript:void(0)" onclick="toggle_bot()" title="Close the virtual assistant"
							class="va-close-btn">×</a>
					</div>
				</div>

				<div id="containerEmp"></div>

			</div>
		</div>
	</div>
	<div class=buttonDiv>
		<a id="botbutton" href="javascript:void(0);" class="botbtn va-inactive" onclick="toggle_bot()">
			<img src="/data/odiebot.svg"
				class="va-trigger-img showHide va-trigger-chat" />
			<img src="/data/cross.svg"
				class="va-trigger-img cross va-trigger-cross" />
		</a>
	</div>
`;

  document.body.appendChild(botDiv);

  const cssLink = document.createElement("link");
  cssLink.rel = "stylesheet";
  cssLink.href = "/data/odiebot.css";
  document.head.appendChild(cssLink);
}

// initial_token is exchanged to another token and saved
async function init_bot(initial_token) {
  let { token, conversationId } = sessionStorage;

  //if (!token) {
  const res = await fetch(
    "https://directline.botframework.com/v3/directline/conversations",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${initial_token}`,
      },
      body: JSON.stringify({
        user: {
          id: "dl_id",
          name: "user",
        },
      }),
    }
  );
  const { token: directLineToken } = await res.json();
  sessionStorage["token"] = directLineToken;
  token = directLineToken;

  if (conversationId) {
    console.log("conversationId: ", conversationId);
    const res = await fetch(
      `https://directline.botframework.com/v3/directline/conversations/${conversationId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    let { conversationId } = await res.json();
    sessionStorage["conversationId"] = conversationId;
  }

  const styleOptions = {
    bubbleBackground: "rgba(248, 248, 248,1)",
    bubbleFromUserBackground: "rgba(207, 238, 255,1)",
    hideUploadButton: true,
    /*Version 4.12*/
    //suggestedActionsStackedLayoutButtonTextWrap: true
    // autoScrollSnapOnActivityOffset: 2
  };
  const directLine = createDirectLine({
    token,
    webSockets: true,
    watermark: 10,
  });
  window.WebChat.renderWebChat(
    {
      directLine: directLine,
      styleOptions,
    },
    document.getElementById("containerEmp")
  );
  document.querySelector("#containerEmp > *").focus();
}

function toggle_bot() {
  div = document.getElementById("va");
  btn = document.getElementById("botbutton");

  if (div.classList.contains("va-show")) {
    div.classList.remove("va-show");
    div.style = "height:0px";
    btn.classList.remove("va-active");
    btn.classList.add("va-inactive");
  } else {
    div.classList.add("va-show");
    div.style = "height:530px;";
    btn.classList.remove("va-inactive");
    btn.classList.add("va-active");
  }
}
