// Validation utility functions

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateRequired = (value: string): boolean => {
  return value.trim().length > 0;
};

export const validateMinLength = (
  value: string,
  minLength: number
): boolean => {
  return value.length >= minLength;
};

export const validateMaxLength = (
  value: string,
  maxLength: number
): boolean => {
  return value.length <= maxLength;
};

export const validateUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const getValidationError = (
  field: string,
  value: string,
  rules: {
    required?: boolean;
    email?: boolean;
    minLength?: number;
    maxLength?: number;
    url?: boolean;
  }
): string | null => {
  if (rules.required && !validateRequired(value)) {
    return `${field} is required`;
  }

  if (rules.email && value && !validateEmail(value)) {
    return `${field} must be a valid email address`;
  }

  if (rules.minLength && value && !validateMinLength(value, rules.minLength)) {
    return `${field} must be at least ${rules.minLength} characters`;
  }

  if (rules.maxLength && value && !validateMaxLength(value, rules.maxLength)) {
    return `${field} must be no more than ${rules.maxLength} characters`;
  }

  if (rules.url && value && !validateUrl(value)) {
    return `${field} must be a valid URL`;
  }

  return null;
};
