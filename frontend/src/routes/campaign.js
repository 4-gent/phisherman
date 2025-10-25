import React from "react";
import DashNav from "../components/dashnavbar";
import '../styles/campaign.css'
import wave from '../styles/images/support_images/wave.svg'

export default function Campaign(){
    return(
        <div className="campaign-body">
            <nav>
                <DashNav />
            </nav>
            <div className="campaign-container">
                <div className="campaign-header">
                    <h1>Let's start a campaign!</h1>
                </div>
                <div className="campaign-content d-flex flex-row justify-content-around">
                    <button className="campaign-button-container">
                        <div className="campaign-button">
                            <p>Financial</p>
                            <p>- </p>
                            <p>Fiscally inspired phishing template</p>
                        </div>
                    </button>
                    <button className="campaign-button-container">
                        <div className="campaign-button">
                            <p>Health </p>
                            <p>- </p>
                            <p>Medically charged phishing template</p>
                        </div>
                    </button>
                    <button className="campaign-button-container">
                        <div className="campaign-button">
                            <p>Personal</p>
                            <p>- </p>
                            <p>Social security based phishing template</p>
                        </div>
                    </button>
                </div>
            </div>
            <img src={wave} className='admin-wave' />
        </div>
    )
}