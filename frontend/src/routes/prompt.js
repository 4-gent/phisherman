import React, { useState, useEffect, useRef } from "react";
import { FaSpinner } from "react-icons/fa";
import "../styles/loading.css";
import "../styles/prompt.css";           // ⬅️ new stylesheet
import { io } from "socket.io-client";
import axios from "axios";
import DashNav from "../components/dashnavbar";

export default function Prompt() {
  const [template, setTemplate] = useState(null);
  const [promptLoad, setPromptLoad] = useState(true);
  const [messages, setMessages] = useState([]); // {role: 'user'|'bot', text: string}
  const [input, setInput] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    try {
      const raw = sessionStorage.getItem("prompt_template");
      if (raw) {
        const tpl = JSON.parse(raw);
        setTemplate(tpl);
      }
    } catch (e) {
      console.warn("failed to read prompt");
    }

    const socket = io("http://localhost:8080", { withCredentials: true });
    socketRef.current = socket;

    socket.on("connect", () => {
      const raw = sessionStorage.getItem("prompt_template");
      if (raw) {
        try {
          const tpl = JSON.parse(raw);
          socket.emit("prompt_inject", { template: tpl });
        } catch (e) {
          console.warn("invalid prompt_template json", e);
        }
      } else {
        socket.emit("prompt_inject", {});
      }
    });

    socket.on("prompt_response", (msg) => {
      if (msg && msg.success && msg.result) {
        setTemplate(msg.result);
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: JSON.stringify(msg.result, null, 2) },
        ]);
      }
      setPromptLoad(false);
    });

    socket.on("chat_response", (msg) => {
      if (msg && msg.success && msg.result) {
        setTemplate(msg.result);
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: JSON.stringify(msg.result, null, 2) },
        ]);
      } else if (msg && msg.error) {
        setMessages((prev) => [
          ...prev,
          { role: "bot", text: `Error: ${msg.error}` },
        ]);
      }
      setPromptLoad(false);
    });

    return () => {
      try {
        socket.disconnect();
      } catch (e) {}
    };
  }, []);

  const sendMessage = () => {
    if (!input) return;
    const msgText = input;
    setMessages((prev) => [...prev, { role: "user", text: msgText }]);
    setInput("");
    setPromptLoad(true);
    const payload = { template, message: msgText };
    try {
      socketRef.current?.emit("chat_message", payload);
    } catch (e) {
      console.warn("socket emit failed", e);
      setPromptLoad(false);
    }
  };

  const sendPromptToApi = async (promptText) => {
    if (!promptText) return;
    try {
      setPromptLoad(true);
      const response = await axios.post(
        "http://localhost:8080/api/prompt/send",
        { prompt: promptText },
        { withCredentials: true }
      );
      if (response && response.data) {
        const botText =
          response.data.result ??
          response.data.message ??
          JSON.stringify(response.data);
        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            text:
              typeof botText === "string"
                ? botText
                : JSON.stringify(botText, null, 2),
          },
        ]);
      }
    } catch (err) {
      console.warn("sendPromptToApi error", err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: `Error sending prompt: ${err?.message ?? err}` },
      ]);
    } finally {
      setPromptLoad(false);
    }
  };

  return (
    <div className="prompt-body">
      <nav>
        <DashNav />
      </nav>
      <div className="prompt-container">
        <header className="prompt-header">
          <div className="prompt-hero">
            <h1 className="prompt-title">Prompt Studio</h1>
            <p className="prompt-subtitle">
              Craft and refine your phishing campaign content in a safe, guided,
              ocean-calm workspace.
            </p>
          </div>
        </header>

        {promptLoad ? (
          <div className="loading-container">
            <FaSpinner className="loading-icon" />
          </div>
        ) : (
          <main className="prompt-main">
            <section className="prompt-panel">
              <div className="prompt-messages">
                {/* If no chat yet, show current working template */}
                {messages.length === 0 && template && (
                  <div className="prompt-template">
                    <pre className="prompt-pre">
                      {typeof template === "string"
                        ? template
                        : JSON.stringify(template, null, 2)}
                    </pre>
                  </div>
                )}

                {/* Conversation */}
                {messages.map((m, i) => (
                  <div
                    key={i}
                    className={`prompt-bubble-row ${
                      m.role === "user"
                        ? "prompt-bubble-row--right"
                        : "prompt-bubble-row--left"
                    }`}
                  >
                    <div
                      className={`prompt-bubble ${
                        m.role === "user"
                          ? "prompt-bubble--user"
                          : "prompt-bubble--bot"
                      }`}
                    >
                      <pre className="prompt-pre">{m.text}</pre>
                      <div className="prompt-bubble-actions">
                        <button
                          className="btn btn-secondary"
                          onClick={() => sendPromptToApi(m.text)}
                          title="Send this version to the campaign API"
                        >
                          Send campaign
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="prompt-input-row">
                <input
                  className="prompt-input"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type a refinement instruction or question…"
                  onKeyDown={(e) => {
                    if (e.key === "Enter") sendMessage();
                  }}
                />
                <button className="btn btn-primary" onClick={sendMessage}>
                  Send
                </button>
              </div>
            </section>

            <aside className="prompt-aside">
              <div className="prompt-card">
                <h3 className="prompt-card-title">Tips</h3>
                <ul className="prompt-tips">
                  <li>Ask for tone tweaks: “More formal” or “friendlier”.</li>
                  <li>
                    Target a department: “Adapt for Finance” or “HR policy”.
                  </li>
                  <li>
                    Add analytics hooks: “Include trackable CTA and preheader”.
                  </li>
                </ul>
              </div>

              <div className="prompt-card alt">
                <h3 className="prompt-card-title">Campaign Goal</h3>
                <p className="prompt-card-text">
                  AI-powered tool that automates phishing email creation and
                  analytics to help run training campaigns and strengthen
                  enterprise security. <em>(Gamified)</em>
                </p>
              </div>
            </aside>
          </main>
        )}
      </div>
    </div>
  );
}
