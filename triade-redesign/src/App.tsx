import Navbar from './components/Navbar'
import Hero from './components/Hero'
import PainPoints from './components/PainPoints'
import About from './components/About'
import Benefits from './components/Benefits'
import Solutions from './components/Solutions'
import Metrics from './components/Metrics'
import UseCases from './components/UseCases'
import Articles from './components/Articles'
import Partners from './components/Partners'
import CtaFinal from './components/CtaFinal'
import Footer from './components/Footer'

function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <PainPoints />
        <About />
        <Benefits />
        <Solutions />
        <Metrics />
        <UseCases />
        <Articles />
        <Partners />
        <CtaFinal />
      </main>
      <Footer />
    </>
  )
}

export default App
