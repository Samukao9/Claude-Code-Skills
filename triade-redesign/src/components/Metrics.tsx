import { useCountUp } from '../hooks/useCountUp'

const metrics = [
  { value: 24, suffix: '/7', label: 'Atendimento Ativo' },
  { value: 90, suffix: '%', label: 'Redução Tarefas Manuais' },
  { value: 3, suffix: 'x', label: 'Mais Leads Qualificados' },
  { value: 50, suffix: '%', label: 'Menos Custo Operacional' },
]

function MetricCard({ value, suffix, label }: { value: number; suffix: string; label: string }) {
  const counter = useCountUp(value, 2000)

  return (
    <div ref={counter.ref} className="glass-card p-8 sm:p-10 text-center group">
      <div className="counter-value font-[Sora] text-5xl sm:text-6xl md:text-7xl font-bold mb-3">
        {counter.value}{suffix}
      </div>
      <p className="text-white/50 text-base font-medium">{label}</p>
    </div>
  )
}

export default function Metrics() {
  return (
    <section id="metricas" className="relative py-24 sm:py-32 px-6 overflow-hidden">
      <div className="orb orb-blue w-[700px] h-[700px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-20" />
      <div className="orb orb-violet w-[500px] h-[500px] -top-20 -right-20 opacity-15" />
      <div className="orb orb-cyan w-[400px] h-[400px] -bottom-20 -left-20 opacity-15" />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
          {metrics.map((m, i) => (
            <MetricCard key={i} {...m} />
          ))}
        </div>
      </div>
    </section>
  )
}
