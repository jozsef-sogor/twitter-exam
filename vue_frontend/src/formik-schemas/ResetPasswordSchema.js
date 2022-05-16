const resetPasswordSchema = [
    {
      $el: 'h3',
      children: 'Reset password'
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
      validation: 'required|length:6,120'
    },
]

export default resetPasswordSchema