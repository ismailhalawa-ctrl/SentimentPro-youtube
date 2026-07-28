'use client';

import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export interface FaqItemData {
  question: string;
  answer: string;
}

interface FaqItemProps {
  item: FaqItemData;
  isOpen: boolean;
  onToggle: () => void;
  index: number;
}

export function FaqItem({ item, isOpen, onToggle, index }: FaqItemProps) {
  const panelId = `faq-panel-${index}`;
  const triggerId = `faq-trigger-${index}`;

  return (
    <Card variant="glass" className="overflow-hidden p-0">
      <button
        id={triggerId}
        onClick={onToggle}
        aria-expanded={isOpen}
        aria-controls={panelId}
        className="flex w-full items-center justify-between gap-4 p-5 text-left"
      >
        <span className="text-base font-medium text-text-primary">{item.question}</span>
        <ChevronDown
          className={cn(
            'h-5 w-5 shrink-0 text-brand-400 transition-transform duration-300',
            isOpen && 'rotate-180'
          )}
        />
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            id={panelId}
            role="region"
            aria-labelledby={triggerId}
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <p className="px-5 pb-5 text-sm text-text-secondary">{item.answer}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
}