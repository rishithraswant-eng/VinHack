"use client";

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function LandingPage({ onLaunch }: { onLaunch: () => void }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    let ctx = gsap.context(() => {
      let isUpdating = false;
      
      // Create a scroll trigger that scrubs the video
      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: "bottom bottom",
        scrub: 2, // Higher value for smoother inertia
        onUpdate: (self) => {
          if (!isUpdating && videoRef.current && Number.isFinite(videoRef.current.duration)) {
            isUpdating = true;
            requestAnimationFrame(() => {
              if (videoRef.current) {
                videoRef.current.currentTime = videoRef.current.duration * self.progress;
              }
              isUpdating = false;
            });
          }
        }
      });
      
      // Animate the launch button to fade in at the very end
      gsap.fromTo(".launch-btn", 
        { opacity: 0, y: 50, pointerEvents: "none" },
        { 
          opacity: 1, 
          y: 0, 
          pointerEvents: "auto",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "bottom 150%", // Trigger when near bottom
            end: "bottom bottom",
            scrub: true
          }
        }
      );
    }, containerRef);
    
    return () => ctx.revert();
  }, []);

  return (
    <div ref={containerRef} className="relative w-full" style={{ height: "600vh", backgroundColor: "#000" }}>
      {/* Sticky container for the video */}
      <div className="sticky top-0 h-screen w-full flex flex-col items-center justify-center overflow-hidden">
        <video 
          ref={videoRef}
          src="/landing.mp4" 
          className="w-full h-full object-cover"
          muted 
          playsInline 
          preload="auto"
        />
        
        {/* Launch Button overlay at the bottom */}
        <div className="absolute bottom-16 w-full flex justify-center launch-btn">
          <button 
            onClick={() => {
              // Scroll to top and then launch so it doesn't stay scrolled down
              window.scrollTo(0, 0);
              onLaunch();
            }}
            className="px-10 py-5 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white rounded-full font-bold text-2xl tracking-widest uppercase transition-all shadow-[0_0_30px_rgba(37,99,235,0.6)] border border-blue-400 backdrop-blur-md hover:scale-105"
          >
            Launch Website
          </button>
        </div>
      </div>
    </div>
  );
}
