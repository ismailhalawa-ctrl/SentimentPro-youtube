import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { FormField } from './form-field';

describe('FormField', () => {
  it('injects id directly onto a bare input child', () => {
    render(
      <FormField label="Email" htmlFor="email-field">
        <input type="email" />
      </FormField>
    );
    const input = screen.getByLabelText('Email');
    expect(input).toHaveAttribute('id', 'email-field');
    expect(document.querySelectorAll('#email-field')).toHaveLength(1);
  });

  it('injects id onto the real control when wrapped in a plain div, not the div itself', () => {
    render(
      <FormField label="YouTube Video URL" htmlFor="youtube-url-primary">
        <div className="relative">
          <input type="url" />
          <span>icon</span>
        </div>
      </FormField>
    );

    const matches = document.querySelectorAll('#youtube-url-primary');
    expect(matches).toHaveLength(1);
    expect(matches[0].tagName).toBe('INPUT');

    const input = screen.getByLabelText('YouTube Video URL');
    expect(input.tagName).toBe('INPUT');
  });

  it('injects id onto the first control when wrapped alongside a sibling element', () => {
    render(
      <FormField label="New Password" htmlFor="reset-password-new">
        <div className="flex flex-col gap-2.5">
          <input type="password" />
          <div data-testid="password-strength">strength meter</div>
        </div>
      </FormField>
    );

    const matches = document.querySelectorAll('#reset-password-new');
    expect(matches).toHaveLength(1);
    expect(matches[0].tagName).toBe('INPUT');
  });

  it("the label's htmlFor points at the real input's id, enabling native click-to-focus", () => {
    render(
      <FormField label="YouTube Video URL" htmlFor="youtube-url-primary">
        <div className="relative">
          <input type="url" />
        </div>
      </FormField>
    );

    const label = screen.getByText('YouTube Video URL').closest('label');
    const input = screen.getByLabelText('YouTube Video URL');
    expect(label).toHaveAttribute('for', 'youtube-url-primary');
    expect(input).toHaveAttribute('id', 'youtube-url-primary');
  });

  it('sets aria-invalid and aria-describedby on the real control when an error is present', () => {
    render(
      <FormField label="Email" htmlFor="email-field" error="Invalid email">
        <input type="email" />
      </FormField>
    );
    const input = screen.getByLabelText('Email');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby', 'email-field-error');
    expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  });

  it('does not set aria-invalid when there is no error', () => {
    render(
      <FormField label="Email" htmlFor="email-field">
        <input type="email" />
      </FormField>
    );
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-invalid', 'false');
  });

  it('renders no error alert when no error is passed', () => {
    render(
      <FormField label="Email" htmlFor="email-field">
        <input type="email" />
      </FormField>
    );
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });
});
