import React from 'react';
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

import type {RenderProps} from './types';

const chipStyle = (accent: string): React.CSSProperties => ({
  display: 'inline-flex',
  alignItems: 'center',
  padding: '12px 18px',
  borderRadius: 999,
  border: `1px solid ${accent}55`,
  background: 'rgba(10, 14, 20, 0.35)',
  color: '#f7f9fb',
  fontSize: 28,
  fontWeight: 600,
  letterSpacing: '0.06em',
  textTransform: 'uppercase',
  backdropFilter: 'blur(10px)',
});

export const ShortsComposition: React.FC<RenderProps> = (props) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const titleSpring = spring({
    fps,
    frame,
    config: {damping: 18, stiffness: 120},
  });
  const supportOpacity = interpolate(frame, [12, 36], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const ctaOpacity = interpolate(frame, [24, 56], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const orbDrift = interpolate(frame, [0, durationInFrames], [0, 120]);

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${props.theme.start} 0%, ${props.theme.end} 100%)`,
        color: '#f7f9fb',
        fontFamily: props.theme.fontFamily,
        overflow: 'hidden',
      }}
    >
      {props.narration.audioSrc ? <Audio src={props.narration.audioSrc} /> : null}

      <AbsoluteFill
        style={{
          opacity: 0.8,
        }}
      >
        <div
          style={{
            position: 'absolute',
            top: 120 - orbDrift * 0.15,
            right: -80,
            width: 460,
            height: 460,
            borderRadius: '50%',
            background: `${props.theme.accent}26`,
            filter: 'blur(8px)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            bottom: 320 + orbDrift * 0.1,
            left: -140,
            width: 520,
            height: 520,
            borderRadius: '50%',
            background: '#ffffff14',
            filter: 'blur(12px)',
          }}
        />
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          padding: '96px 84px',
          justifyContent: 'space-between',
        }}
      >
        <div style={{display: 'flex', justifyContent: 'space-between', gap: 24}}>
          <div style={chipStyle(props.theme.accent)}>{props.theme.badge}</div>
          <div style={chipStyle(props.theme.accent)}>
            {props.platforms.map((platform) => platform.replace('_', ' ')).join(' / ')}
          </div>
        </div>

        <div style={{display: 'flex', flexDirection: 'column', gap: 34}}>
          <div
            style={{
              fontSize: 122,
              lineHeight: 0.94,
              fontWeight: 800,
              letterSpacing: '-0.05em',
              transform: `translateY(${(1 - titleSpring) * 120}px) scale(${0.96 + titleSpring * 0.04})`,
              opacity: titleSpring,
              maxWidth: 920,
            }}
          >
            {props.hook.title}
          </div>

          <div
            style={{
              fontSize: 46,
              lineHeight: 1.3,
              maxWidth: 860,
              color: '#eef3f7',
              opacity: supportOpacity,
            }}
          >
            {props.hook.support}
          </div>
        </div>

        <div style={{display: 'flex', flexDirection: 'column', gap: 28}}>
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: 18,
            }}
          >
            {props.hook.visualMotifs.map((motif) => (
              <div key={motif} style={chipStyle(props.theme.accent)}>
                {motif}
              </div>
            ))}
          </div>

          <div
            style={{
              fontSize: 42,
              fontWeight: 700,
              color: props.theme.accent,
              opacity: ctaOpacity,
            }}
          >
            {props.hook.cta}
          </div>
        </div>
      </AbsoluteFill>

      {props.captions.map((caption, index) => {
        const startFrom = Math.floor((durationInFrames / Math.max(props.captions.length, 1)) * index);
        return (
          <Sequence key={`${caption}-${index}`} from={startFrom} durationInFrames={durationInFrames - startFrom}>
            <div
              style={{
                position: 'absolute',
                bottom: 170,
                left: 72,
                right: 72,
                display: 'flex',
                justifyContent: 'center',
              }}
            >
              <div
                style={{
                  padding: '22px 30px',
                  borderRadius: 28,
                  background: 'rgba(8, 10, 14, 0.58)',
                  border: `1px solid ${props.theme.accent}44`,
                  fontSize: 36,
                  fontWeight: 700,
                  textAlign: 'center',
                  lineHeight: 1.25,
                  maxWidth: 936,
                }}
              >
                {caption}
              </div>
            </div>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
