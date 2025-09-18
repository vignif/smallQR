# SmallQR Web App

<p align="left">
  <a href="https://github.com/vignif/smallQR/actions/workflows/test.yml">
    <img alt="CI Status" src="https://github.com/vignif/smallQR/actions/workflows/test.yml/badge.svg" />
  </a>
  <a href="https://coveralls.io/github/vignif/smallQR?branch=main">
    <img alt="Coverage Status" src="https://coveralls.io/repos/github/vignif/smallQR/badge.svg?branch=main" />
  </a>
  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/vignif/smallQR.svg" />
</p>

SmallQR is a web application that allows users to create the smallest QR code given their input data. The generated QR code is held in memory, not stored on the disk. Users can customize settings such as error correction level and QR code version.

## Features

- Minimal QR code generation
- Customizable error correction level
- QR code version selection
- In-memory storage (no disk storage)

## Privacy & GDPR

This application is designed with data minimization:

- User input is processed transiently in memory only to generate a QR code and is not persisted.
- A short-lived session value stores only a captcha answer (anti-abuse).
- No analytics, tracking, or marketing cookies.
- Aggregate counter tracks only total number of QR codes generated.
- Security headers (CSP / Referrer-Policy / etc.) are applied.
- Cloudflare reverse proxy adds DDoS protection; IP & UA appear in security logs (retained ≤ 30 days).
- Basic rate limiting (Flask-Limiter) mitigates automated abuse.

See the dedicated [Privacy page](/privacy) in the running app for full details (legal basis, retention, rights, third parties).



## App Available on a VPS

[![Live App](https://img.shields.io/badge/Demo-Click%20Here-blue.svg)](https://apps.francescovigni.com/smallqr/)

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:vignif/smallQR.git

<p align="left">
  <img alt="Python Version" src="https://img.shields.io/badge/Python-3.9-blue.svg" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg" />
</p>
