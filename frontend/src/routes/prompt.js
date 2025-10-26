import React, {useState, useEffect, useRef} from "react";
import {FaSpinner} from "react-icons/fa"
import '../styles/loading.css'
import { io } from "socket.io-client";
import axios from "axios";

export default function Prompt(){
    const [template, setTemplate] = useState(null)
    const [promptLoad, setPromptLoad] = useState(true)
    const [messages, setMessages] = useState([]) // {role: 'user'|'bot', text: string}
    const [input, setInput] = useState('')
    const socketRef = useRef(null)



    useEffect(() => {
        try{
            const raw = sessionStorage.getItem('prompt_template')
            if(raw){
                const tpl = JSON.parse(raw)
                setTemplate(tpl)
            }
        } catch (e) {
            console.warn('failed to read prompt')
        }

        const socket = io('http://localhost:8080', {withCredentials: true})
        socketRef.current = socket

        socket.on('connect', () => {
            console.log('socket connected', socket.id)
            const raw = sessionStorage.getItem('prompt_template')
            if (raw){
                try{
                    const tpl = JSON.parse(raw)
                    socket.emit('prompt_inject', {template: tpl})
                } catch (e) {
                    console.warn('invalid prompt_template json', e)
                }
            } else {
                socket.emit('prompt_inject', {})
            }
        })

        socket.on('prompt_response', (msg) => {
            console.log('prompt_response', msg)
            if (msg && msg.success && msg.result) {
                setTemplate(msg.result)
                setMessages(prev => [...prev, {role:'bot', text: JSON.stringify(msg.result, null, 2)}])
            }
            setPromptLoad(false)
        })

        socket.on('chat_response', (msg) => {
            console.log('chat_response', msg)
            if (msg && msg.success && msg.result) {
                // update template and append bot message
                setTemplate(msg.result)
                setMessages(prev => [...prev, {role:'bot', text: JSON.stringify(msg.result, null, 2)}])
            } else if (msg && msg.error) {
                setMessages(prev => [...prev, {role:'bot', text: `Error: ${msg.error}`}])
            }
            setPromptLoad(false)
        })

        return () => {
            try { socket.disconnect() } catch(e) {}
        }
    }, [])

    const sendMessage = () => {
        if(!input) return
        const msgText = input
        setMessages(prev => [...prev, {role:'user', text: msgText}])
        setInput('')
        setPromptLoad(true)
        const payload = { template, message: msgText }
        try {
            socketRef.current?.emit('chat_message', payload)
        } catch(e) {
            console.warn('socket emit failed', e)
            setPromptLoad(false)
        }
    }

    const sendPromptToApi = async(promptText) => {
        if(!promptText) return
        try{
            setPromptLoad(true)
            const response = await axios.post('http://localhost:8080/api/prompt/send', 
                {prompt: promptText}, 
                {withCredentials: true}
            )
            if (response && response.data){
                const botText = response.data.result ?? response.data.message ?? JSON.stringify(response.data)
                setMessages(prev => [...prev, {role: 'bot', text: typeof botText === 'string' ? botText : JSON.stringify(botText, null, 2)}])
            }
        } catch (err) {
            console.warn('sendPromptToApi error', err)
            setMessages(prev => [...prev, {role: 'bot', text: `Error sending prompt: ${err?.message ?? err}`}])
        } finally {
            setPromptLoad(false)
        }
    }

    return(
        <div>
            {promptLoad ? (
                <div className='loading-container'>
                    <FaSpinner className="loading-icon" />
                </div>
            ) : (
                <div>
                    <div style={{maxHeight: '40vh', overflowY: 'auto', border: '1px solid #ddd', padding: 10, marginBottom: 10}}>
                        {messages.length === 0 && template && (
                            <pre style={{whiteSpace: 'pre-wrap', wordBreak: 'break-word'}}>
                                {typeof template === 'string' ? template : JSON.stringify(template, null, 2)}
                            </pre>
                        )}
                        {messages.map((m, i) => (
                            <div key={i} style={{textAlign: m.role === 'user' ? 'right' : 'left', margin: '6px 0'}}>
                                <div style={{display:'inline-block', padding:8, borderRadius:6, background: m.role==='user' ? '#cfe9ff' : '#eef2ff', maxWidth:'80%'}}>
                                    <pre style={{margin:0, whiteSpace:'pre-wrap', wordBreak:'break-word'}}>{m.text}</pre>
                                </div>
                                <div style={{marginTop: 6}}>
                                    <button onClick={() => sendPromptToApi(m.text)} style={{fontSize: 12, padding: '4px 8px'}}>Send campaign</button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{display:'flex', gap:8}}>
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type a refinement instruction or question..."
                            style={{flex:1, padding:8}}
                            onKeyDown={(e) => { if(e.key === 'Enter') sendMessage() }}
                        />
                        <button onClick={sendMessage}>Send</button>
                    </div>
                </div>
            )}
        </div>
    )
}