'use client';

import { motion } from 'framer-motion';
import { useVideoInfo } from '../../features/youtube/hooks/use-video-info';
import { FetchStatus } from './fetch-status';
import { VideoMetadataCard } from './video-metadata-card';

interface VideoPreviewProps {
  url: string;
  compareUrl?: string;
  mode: 'single' | 'compare';
}

export function VideoPreview({ url, compareUrl, mode }: VideoPreviewProps) {
  const { data: videoA, isLoading: loadingA, error: errorA } = useVideoInfo(url);
  const { data: videoB, isLoading: loadingB, error: errorB } = useVideoInfo(compareUrl || '');

  const isCompare = mode === 'compare';

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="flex flex-col gap-4"
    >
      {loadingA || errorA ? (
        <FetchStatus 
          isLoading={loadingA} 
          error={errorA} 
          loadingLabel="Fetching Video A details…" 
        />
      ) : videoA ? (
        <VideoMetadataCard video={videoA} />
      ) : null}

      {isCompare && compareUrl && compareUrl.trim().length > 0 && (
        <>
          {loadingB || errorB ? (
            <FetchStatus 
              isLoading={loadingB} 
              error={errorB} 
              loadingLabel="Fetching Video B details…" 
            />
          ) : videoB ? (
            <VideoMetadataCard video={videoB} />
          ) : null}
        </>
      )}
    </motion.div>
  );
}