const registerSchema = [
    {
      $el: 'h3',
      children: 'Sign up'
    },
    {
      $formkit: 'text',
      name: 'user_name',
      label: 'User name',
      help: 'This will be used for your account.',
      validation: 'required'
    },
    {
      $formkit: 'text',
      name: 'user_first_name',
      label: 'First name',
      help: 'This will be used for your account.',
      validation: 'required'
    },
    {
      $formkit: 'text',
      name: 'user_last_name',
      label: 'Last name',
      help: 'This will be used for your account.',
      validation: 'required'
    },
    {
      $formkit: "file",
      label: "Profile picture",
      name: "user_image",
      accept: ".png, .jpg, .jpeg, webp",
      help: "Select a picture you like.",
    },
    {
      $formkit: 'text',
      name: 'user_email',
      label: 'Email',
      help: 'This will be used for your account.',
      validation: 'required|email'
    },
    {
      $formkit: 'password',
      name: 'user_password',
      label: 'Password',
      help: 'Enter your new password.',
      validation: 'required|length:6,120'
    },
    {
      $formkit: 'password',
      name: 'user_password_again',
      label: 'Password',
      help: 'Enter your new password.',
      validation: 'required'
    },
]

export default registerSchema