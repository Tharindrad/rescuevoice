import { useEffect, useState } from 'react'
import {
  ConversationProvider,
  useConversationControls,
  useConversationStatus,
  useConversation,
} from '@elevenlabs/react'
import { Mic, PhoneOff, Loader2, ShieldCheck, AlertTriangle } from 'lucide-react'
import { getElevenLabsSignedUrl } from '../services/api'

type Props = {
  applicationId: string
  applicant: string
  language: string
  onClose: () => void
}

function VoiceSession({ applicationId, applicant, language, onClose }: Props) {
  const { startSession, endSession } = useConversationControls()
  const { status } = useConversationStatus()
  const conversation = useConversation({
    onError: (error) => setError(error instanceof Error ? error.message : String(error)),
  })
  const [error, setError] = useState('')
  const [starting, setStarting] = useState(false)
  const [transcript, setTranscript] = useState<string[]>([])

  useEffect(() => {
    return () => {
      try { endSession() } catch {}
    }
  }, [endSession])

  const start = async () => {
    setStarting(true)
    setError('')
    try {
      const permission = await navigator.mediaDevices.getUserMedia({ audio: true })
      permission.getTracks().forEach(t => t.stop())

      const signedUrl = await getElevenLabsSignedUrl()
      await startSession({
        signedUrl,
        userId: applicationId,
      })
    } catch (e: any) {
      setError(e?.message || 'Unable to start the ElevenLabs session.')
    } finally {
      setStarting(false)
    }
  }

  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent).detail
      if (detail?.message) setTranscript(prev => [...prev.slice(-5), detail.message])
    }
    window.addEventListener('rescuevoice:agent-message', handler)
    return () => window.removeEventListener('rescuevoice:agent-message', handler)
  }, [])

  const connected = status === 'connected'
  const connecting = status === 'connecting' || starting

  return (
    <div className="fixed inset-0 z-50 bg-black/35 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white rounded-3xl shadow-2xl overflow-hidden">
        <div className="p-6 border-b border-zinc-100 flex items-center justify-between">
          <div>
            <div className="text-[10px] uppercase tracking-[.18em] text-zinc-400">ElevenLabs Live Agent</div>
            <h2 className="text-xl font-bold mt-1">Rescue call · {applicationId}</h2>
            <p className="text-xs text-zinc-500 mt-1">{applicant} · {language}</p>
          </div>
          <button onClick={onClose} className="px-3 py-2 rounded-xl bg-zinc-100 text-xs font-semibold">Close</button>
        </div>

        <div className="p-6">
          <div className="rounded-2xl bg-zinc-950 text-white p-7 text-center">
            <div className={`mx-auto w-20 h-20 rounded-full grid place-items-center ${connected ? 'bg-emerald-500/20' : 'bg-white/10'}`}>
              {connecting ? <Loader2 className="animate-spin" size={30}/> : connected ? <Mic size={30}/> : <Mic size={30}/>}
            </div>
            <div className="mt-4 font-bold">{connected ? 'Voice conversation active' : connecting ? 'Connecting securely…' : 'Ready to call'}</div>
            <div className="text-xs text-zinc-400 mt-1">
              {connected ? 'ElevenLabs ↔ RescueVoice Harness' : 'Your browser microphone will be requested'}
            </div>

            {!connected && !connecting && (
              <button onClick={start} className="mt-6 px-5 py-3 rounded-xl bg-white text-zinc-950 font-bold text-sm">
                Start secure voice session
              </button>
            )}
            {connected && (
              <button onClick={() => endSession()} className="mt-6 px-5 py-3 rounded-xl bg-red-500 text-white font-bold text-sm inline-flex items-center gap-2">
                <PhoneOff size={16}/> End call
              </button>
            )}
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3">
            <div className="border rounded-2xl p-4">
              <div className="flex items-center gap-2 text-xs font-bold"><ShieldCheck size={15}/> API key safety</div>
              <p className="text-[11px] text-zinc-500 mt-1">Key stays server-side. Browser receives only a temporary signed URL.</p>
            </div>
            <div className="border rounded-2xl p-4">
              <div className="text-xs font-bold">Case boundary</div>
              <p className="text-[11px] text-zinc-500 mt-1">{applicationId} is the conversation context.</p>
            </div>
          </div>

          {transcript.length > 0 && (
            <div className="mt-4 rounded-2xl bg-zinc-50 p-4">
              <div className="text-[10px] uppercase tracking-wider text-zinc-400 mb-2">Live messages</div>
              {transcript.map((line, i) => <div key={i} className="text-xs py-1">{line}</div>)}
            </div>
          )}

          {error && (
            <div className="mt-4 p-4 rounded-2xl bg-red-50 text-red-700 text-xs flex gap-2">
              <AlertTriangle size={16}/><span>{error}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export function VoiceCall({ applicationId, applicant, language, onClose }: Props) {
  return (
    <ConversationProvider
      onConnect={() => window.dispatchEvent(new CustomEvent('rescuevoice:connected'))}
      onDisconnect={() => window.dispatchEvent(new CustomEvent('rescuevoice:disconnected'))}
      onError={(error) => window.dispatchEvent(new CustomEvent('rescuevoice:error', { detail: String(error) }))}
    >
      <VoiceSession applicationId={applicationId} applicant={applicant} language={language} onClose={onClose}/>
    </ConversationProvider>
  )
}
