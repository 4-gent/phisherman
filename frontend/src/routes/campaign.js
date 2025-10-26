import React from "react";
import axios from "axios";
import DashNav from "../components/dashnavbar";
import '../styles/campaign.css'
import wave from '../styles/images/support_images/wave.svg'
import { ToastContainer, toast } from "react-toastify";

export default function Campaign(){
    const handleTemplate = async(template) => {
        try{
            console.log("template", template)
            const response = await axios.post(
                'http://localhost:8080/api/campaign',
                {template},
                {withCredentials: true}
            )
            if(response && response.status === 200){
                try {
                    sessionStorage.setItem('prompt_template', JSON.stringify(response.data.template))
                } catch(e) {
                    console.warn('could not store: ', e)
                }
                toast.success('Sending to prompt engine', {autoClose: 1500})
                window.location.href='/prompt'
            }
            console.log(response.data.template)
        } catch (err) {
            console.log("Campaign reponse: ", err)
        }
    }
    
    return(
        <div className="campaign-body">
            <nav>
                <DashNav />
            </nav>
            <div className="campaign-container">
                <img src={wave} className='admin-wave' />
                <div className="campaign-header">
                    <h1 className="campaign-header-text">Let's start a campaign!</h1>
                </div>
                <div className="campaign-content d-flex flex-row justify-content-around">
                    <button type='button' className="campaign-button-container" onClick={() => handleTemplate('financial')}>
                        <div className="campaign-button">
                            <p style={{fontSize: '2em', fontWeight: 'bold'}}>Financial</p>
                            <p>- </p>
                            <p style={{fontSize: '1.2em'}}>Fiscally inspired phishing template</p>
                        </div>
                    </button>
                    <button type='button' className="campaign-button-container" onClick={() => handleTemplate('health')}>
                        <div className="campaign-button">
                            <p style={{fontSize: '2em', fontWeight: 'bold'}}>Health </p>
                            <p>- </p>
                            <p style={{fontSize: '1.2em'}}>Medically charged phishing template</p>
                        </div>
                    </button>
                    <button type='button' className="campaign-button-container" onClick={() => handleTemplate('personal')}>
                        <div className="campaign-button">
                            <p style={{fontSize: '2em', fontWeight: 'bold'}}>Personal</p>
                            <p>- </p>
                            <p style={{fontSize: '1.2em'}}>Social security based phishing template</p>
                        </div>
                    </button>
                </div>
            </div>
            <ToastContainer />
        </div>
    )
}