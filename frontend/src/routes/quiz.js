import React from 'react'
import '../styles/quiz.css'
import fisherman from '../styles/images/fishing.png'

//game page

export default function Quiz(){
    return(
        <div className='quiz-body'>
            <div className='d-flex flex-row justify-content-between'>
                <img src={fisherman} alt="fisherman" className='fisherman-image'/>
            </div>
            {/* backgrund image */}
            {/* fish images */}
            {/* score box */}
        </div>
    )
}