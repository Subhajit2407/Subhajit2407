import React from 'react'
import { createRoot } from 'react-dom/client'
import ContributionSkyline from '../src/components/ui/contribution-skyline'
import contributions from '../data/contributions.json'
import dashboard from '../data/dashboard.json'
import './styles.css'

const days = contributions.days.map(({ date, count }) => ({ date, count }))
function App() {
  return <main className="dashboard">
    <nav><a href="https://github.com/Subhajit2407">github.com/<strong>Subhajit2407</strong></a><span><a href="#about">&lt; About /&gt;</a><a href="#skills">&lt; Skills /&gt;</a><a href="#projects">&lt; Projects /&gt;</a><a href="#contact">&lt; Contact /&gt;</a></span></nav>
    <img src="/assets/banner.svg" className="panel" alt="Subhajit Talukder, Software Development Engineer — Backend, Full Stack, AI" />
    <section id="about" className="identity"><img src="/assets/portrait.svg" alt="Animated ASCII portrait of Subhajit"/><img src="/assets/neofetch.svg" alt="Engineering profile and education"/></section>
    <section id="skills"><img className="panel" src="/assets/tech-stack.svg" alt="Technical skills grouped by languages, backend, frontend, databases, cloud and AI"/></section>
    <section className="skyline"><ContributionSkyline data={days} endDate={contributions.to} palette="github" defaultView="3d" title="Contribution Skyline / Subhajit2407" footer="Actual public GitHub activity · Switch views or drag to orbit"/></section>
    <section id="projects"><h2>// FEATURED PROJECTS</h2><div className="projects">{dashboard.projects.map(p=><article key={p.id}>{p.link?<a href={p.link}><img src={'/assets/projects/'+p.id+'.svg'} alt={p.name+' — '+p.description.join(' ')}/></a>:<img src={'/assets/projects/'+p.id+'.svg'} alt={p.name+' — '+p.description.join(' ')}/>}</article>)}</div></section>
    <img className="panel" src="/assets/impact.svg" alt="Engineering impact from resume: 100+ users, 30% faster APIs, 3 deployed applications, AI and CI/CD"/>
    <footer id="contact"><a href="https://github.com/Subhajit2407">GitHub ↗</a><a href="https://www.linkedin.com/in/subhajit-talukder-b73bb229b/">LinkedIn ↗</a><a href={dashboard.portfolio}>Portfolio ↗</a><a href={'mailto:'+dashboard.email}>Email ↗</a><p>create. iterate. build.</p></footer>
  </main>
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>)
