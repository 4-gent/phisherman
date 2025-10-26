import React from 'react';
import { Link } from 'react-router-dom';
import './styles/main.css';
import Navigation from './components/navbar';
import wave from './styles/images/support_images/wave2.svg';
import fish from './styles/images/fish1.png';

export default function Main() {
  return (
    <div className="main-body">
      <nav>
        <Navigation />
      </nav>

      <div className="main-container">
        {/* Hero Section */}
        <section className="main-hero">
          <img src={wave} alt="wave" className="main-wave" />
          <div className="main-hero-text">
            <h1 className="main-title">Phisherman</h1>
            <p className="main-subtitle">Reeling in Security Awareness</p>
          </div>
          <div className="main-hero-art">
            <img src={fish} alt="fishing art" className="main-fish" />
          </div>
        </section>

        {/* Project Description */}
        <section className="main-about">
          <div className="main-about-content">
            <h2>Automate. Analyze. Educate.</h2>
            <p>
              <strong>Phisherman</strong> is an AI-powered cybersecurity training platform that automates
              phishing email creation and analytics to strengthen enterprise security. Designed for modern
              organizations, it allows administrators to launch phishing simulation campaigns, monitor user
              interactions, and measure awareness improvement over time.
            </p>
            <p>
              Employees receive realistic, tailored phishing emails — powered by intelligent content generation
              — and learn to identify and report threats in a safe, gameified environment. Administrators gain
              access to performance dashboards and behavioral insights, helping them make smarter, data-driven
              decisions about future training.
            </p>
            <p className="main-highlight">
              The goal: create a safer digital workplace by turning employees from the weakest link into the
              first line of defense.
            </p>
          </div>
        </section>

        {/* CTA / Footer */}
        <section className="main-cta">
          <h2>Ready to Cast Your First Campaign?</h2>
          <Link to="/login" className="main-btn">
            Dive In
          </Link>
        </section>
      </div>
    </div>
  );
}
