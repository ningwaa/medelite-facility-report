The application is completely live and accessible at https://medelite-facility-report-zwjr.onrender.com/.

Honestly, I kept this project very practical since it was a 5–6 hour MVP. I didn’t use real APIs or external datasets, and instead worked with simple made-up/sample data to test the functionality.
I followed the given instructions closely and focused more on building a working end-to-end system rather than setting up complex data sourcing or integrations.
My main assumption was that sample data would be enough to demonstrate the reporting logic and overall workflow, and I prioritized making sure the application worked correctly over adding advanced data pipelines or external connections.

#TechStack
Backend Framework: Flask
PDF Generation & Reporting: ReportLab
Deployment & Hosting Platform: Render
Version Control & CI/CD Trigger: Git / GitHub
Development Environment: macOS Terminal & VS Code

The main issue was deployment failures caused by missing dependencies (Flask and ReportLab), cached builds on the server, and a port configuration error. To fix it, I updated the requirements.txt,
cleared the deployment cache to force a clean rebuild, and changed the app to use the correct environment port (os.environ.get("PORT")). I also fixed a small code indentation issue, which finally allowed the application to deploy successfully.
