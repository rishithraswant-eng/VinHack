"use client";

import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import { ChevronDown, ShieldAlert, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function LandingPage({ onLaunch }: { onLaunch: () => void }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [scrollHintVisible, setScrollHintVisible] = useState(true);

  useEffect(() => {
    // 1. Initialize Lenis for buttery-smooth momentum scrolling
    const lenis = new Lenis({
      duration: 1.4,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1.1,
      touchMultiplier: 1.8,
    });

    // Sync Lenis scroll updates with GSAP ScrollTrigger
    lenis.on('scroll', ScrollTrigger.update);

    const updateLenis = (time: number) => {
      lenis.raf(time * 1000);
    };
    gsap.ticker.add(updateLenis);
    gsap.ticker.lagSmoothing(0);

    let ctx = gsap.context(() => {
      const video = videoRef.current;
      if (!video) return;

      const initScrollScrub = () => {
        const dur = Number.isFinite(video.duration) && video.duration > 0 ? video.duration : 10.08;
        const playhead = { time: 0 };
        let isSeekingFrame = false;
        let pendingTime = 0;

        // GSAP tween for the playhead - scrub: 1.0 creates silky smooth inertia
        gsap.to(playhead, {
          time: dur,
          ease: "none",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top top",
            end: "bottom bottom",
            scrub: 1.0,
            onUpdate: (self) => {
              if (self.progress > 0.05) {
                setScrollHintVisible(false);
              } else {
                setScrollHintVisible(true);
              }
            }
          },
          onUpdate: () => {
            pendingTime = playhead.time;
            if (!isSeekingFrame) {
              isSeekingFrame = true;
              requestAnimationFrame(() => {
                if (video && Number.isFinite(pendingTime)) {
                  video.currentTime = pendingTime;
                }
                isSeekingFrame = false;
              });
            }
          }
        });

        // Launch button animation at the end of the scroll
        gsap.fromTo(
          ".launch-btn-container",
          { opacity: 0, scale: 0.85, y: 60, pointerEvents: "none" },
          {
            opacity: 1,
            scale: 1,
            y: 0,
            pointerEvents: "auto",
            ease: "power2.out",
            scrollTrigger: {
              trigger: containerRef.current,
              start: "bottom 135%",
              end: "bottom bottom",
              scrub: 0.8,
            }
          }
        );
      };

      if (video.readyState >= 1 && Number.isFinite(video.duration)) {
        initScrollScrub();
      } else {
        video.addEventListener('loadedmetadata', initScrollScrub, { once: true });
      }
    }, containerRef);

    return () => {
      gsap.ticker.remove(updateLenis);
      lenis.destroy();
      ctx.revert();
    };
  }, []);

  const handleLaunch = () => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    onLaunch();
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full select-none bg-black"
      style={{ height: "650vh" }}
    >
      {/* Sticky Fullscreen Video Player */}
      <div className="sticky top-0 h-screen w-full flex flex-col items-center justify-center overflow-hidden bg-black">
        <video
          ref={videoRef}
          src="/landing.mp4"
          className="w-full h-full object-cover pointer-events-none"
          muted
          playsInline
          preload="auto"
          autoPlay={false}
        />

        {/* Top Header Branding Overlay */}
        <div className="absolute top-8 left-8 flex items-center gap-3 pointer-events-none z-20">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center backdrop-blur-md shadow-[0_0_20px_rgba(59,130,246,0.3)]">
            <ShieldAlert className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <div className="text-xl font-extrabold tracking-widest text-white uppercase flex items-center gap-2">
              PHANTASM
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
                PRO-DEFENSE
              </span>
            </div>
            <p className="text-xs text-slate-400 tracking-wider">AI Cryptographic Asset Tracing Engine</p>
          </div>
        </div>

        {/* Scroll down guidance indicator */}
        <div
          className={`absolute bottom-12 flex flex-col items-center gap-2 pointer-events-none transition-all duration-700 ${
            scrollHintVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <div className="px-5 py-2 rounded-full bg-black/60 border border-white/10 backdrop-blur-md flex items-center gap-2 shadow-2xl">
            <span className="text-xs font-semibold tracking-widest text-slate-300 uppercase">Scroll to Explore</span>
            <ChevronDown className="w-4 h-4 text-blue-400 animate-bounce" />
          </div>
        </div>

        {/* Launch Website Button Overlay */}
        <div className="absolute bottom-20 w-full flex flex-col items-center justify-center gap-4 launch-btn-container z-30">
          <button
            onClick={handleLaunch}
            className="group relative px-12 py-5 rounded-full font-extrabold text-xl tracking-wider text-white uppercase overflow-hidden shadow-[0_0_50px_rgba(37,99,235,0.7)] transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer"
          >
            {/* Animated Glow Border & Gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 transition-all duration-300 group-hover:opacity-90" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.35),transparent_70%)]" />
            <div className="absolute inset-[1px] rounded-full bg-slate-950/40 backdrop-blur-md -z-0" />
            
            <span className="relative z-10 flex items-center gap-3">
              <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse" />
              Launch Forensic Suite
            </span>
          </button>
          <p className="text-xs text-slate-400 font-mono tracking-widest uppercase">
            Sec 94 BNSS &bull; 65B IT Act Certified
          </p>
        </div>
      </div>
    </div>
  );
}
