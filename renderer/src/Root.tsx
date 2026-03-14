import React from 'react';
import {Composition} from 'remotion';

import {ShortsComposition} from './ShortsComposition';
import type {RenderProps} from './types';

const defaultProps: RenderProps = {
  compositionId: 'ShortsMakerVertical',
  jobId: 'preview',
  language: {
    code: 'en',
    label: 'English',
  },
  platforms: ['tiktok', 'instagram_reels', 'facebook_reels'],
  video: {
    width: 1080,
    height: 1920,
    fps: 30,
    durationInFrames: 330,
  },
  theme: {
    brandLabel: 'Saju Signal',
    badge: 'SAJU SIGNAL',
    fontFamily: "'Aptos', 'Segoe UI', sans-serif",
    start: '#121c2c',
    end: '#5f7da9',
    accent: '#f4fbff',
  },
  hook: {
    title: 'Your strong Metal energy is cutting off your money flow.',
    support: 'Water day masters recover when Wood comes back into balance.',
    cta: 'Save this before your next luck shift.',
    keywords: ['metal', 'wood', 'money'],
    visualMotifs: ['clarity', 'signal', 'growth'],
    traits: ['sharp judgment'],
  },
  captions: [
    'Your strong Metal energy',
    'is cutting off your money flow.',
    'Save this before your next luck shift.',
  ],
  narration: {
    audioSrc: null,
    durationSeconds: 11,
    voice: 'en-US-AriaNeural',
  },
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ShortsMakerVertical"
      component={ShortsComposition}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={defaultProps.video.durationInFrames}
      defaultProps={defaultProps}
      calculateMetadata={({props}) => {
        const typedProps = props as RenderProps;
        return {
          durationInFrames: typedProps.video.durationInFrames,
          width: typedProps.video.width,
          height: typedProps.video.height,
          fps: typedProps.video.fps,
        };
      }}
    />
  );
};
