import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ExportMenu } from './export-menu';

const exportAsMock = vi.fn();

vi.mock('@/features/analysis/hooks/use-export-analysis', () => ({
  useExportAnalysis: () => ({ exportAs: exportAsMock, isExporting: false }),
}));

describe('ExportMenu', () => {
  beforeEach(() => {
    exportAsMock.mockClear();
  });

  it('opens the menu when the trigger is clicked', async () => {
    const user = userEvent.setup();
    render(<ExportMenu jobId={1} filenameHint="video" />);

    expect(screen.queryByRole('menu')).not.toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /export/i }));
    expect(screen.getByRole('menu')).toBeInTheDocument();
  });

  it('closes the menu and returns focus to the trigger on Escape', async () => {
    const user = userEvent.setup();
    render(<ExportMenu jobId={1} filenameHint="video" />);

    const trigger = screen.getByRole('button', { name: /export/i });
    await user.click(trigger);
    expect(screen.getByRole('menu')).toBeInTheDocument();

    fireEvent.keyDown(document, { key: 'Escape' });

    await waitFor(() => expect(screen.queryByRole('menu')).not.toBeInTheDocument());
    expect(document.activeElement).toBe(trigger);
  });

  it('closes the menu when clicking outside', async () => {
    const user = userEvent.setup();
    render(
      <div>
        <ExportMenu jobId={1} filenameHint="video" />
        <button>outside</button>
      </div>
    );

    await user.click(screen.getByRole('button', { name: /export/i }));
    expect(screen.getByRole('menu')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'outside' }));
    await waitFor(() => expect(screen.queryByRole('menu')).not.toBeInTheDocument());
  });

  it('calls exportAs with the selected format and closes the menu', async () => {
    const user = userEvent.setup();
    render(<ExportMenu jobId={42} filenameHint="my-video" />);

    await user.click(screen.getByRole('button', { name: /export/i }));
    await user.click(screen.getByRole('menuitem', { name: /csv/i }));

    expect(exportAsMock).toHaveBeenCalledWith(42, 'csv', 'my-video');
    await waitFor(() => expect(screen.queryByRole('menu')).not.toBeInTheDocument());
  });

  it('does not respond to Escape when the menu is already closed', () => {
    render(<ExportMenu jobId={1} filenameHint="video" />);
    expect(() => fireEvent.keyDown(document, { key: 'Escape' })).not.toThrow();
  });
});
