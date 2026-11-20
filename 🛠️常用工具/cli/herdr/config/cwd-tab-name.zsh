# Rename generated tabs once at startup, then whenever this shell changes cwd.
if [[ ${HERDR_ENV:-} == 1 ]]; then
  _herdr_cwd_tab_name() {
    command python3 "$HOME/.config/herdr/cwd-tab-name.py" "$PWD" "${_herdr_tab_previous_cwd:-$PWD}" >/dev/null 2>&1
    typeset -g _herdr_tab_previous_cwd=$PWD
    return 0
  }
  _herdr_cwd_tab_init() {
    _herdr_cwd_tab_name
    add-zsh-hook -d precmd _herdr_cwd_tab_init
  }
  autoload -Uz add-zsh-hook
  add-zsh-hook chpwd _herdr_cwd_tab_name
  add-zsh-hook precmd _herdr_cwd_tab_init
fi
