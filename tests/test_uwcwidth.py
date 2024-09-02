import pytest

from uwcwidth import wcswidth, wcwidth, wcwidth_uint32, is_EMB, is_EMB_uint32


class TestSimple:
    def test_empty(self):
        assert wcswidth('') == 0

    def test_wcwidth_only_one_codepoint(self):
        with pytest.raises(ValueError):
            wcwidth('')

        with pytest.raises(ValueError):
            wcwidth('ab')

    def test_simple_ascii(self):
        assert wcswidth('Hello!') == 6
        assert wcswidth('!') == 1
        assert wcswidth('a~@!#~Z') == 7

        assert wcwidth('!') == 1
        assert wcwidth_uint32(ord('!')) == 1

        assert wcwidth('a') == 1
        assert wcwidth_uint32(ord('a')) == 1

    def test_ascii_nonprintables(self):
        assert wcwidth('\001') == -1
        assert wcwidth('\033') == -1
        assert wcwidth('\r') == -1
        assert wcwidth('\n') == -1
        assert wcwidth('\000') == 0

        assert wcswidth('Hi\tthere') == -1
        assert wcswidth('There is an \033') == -1
        assert wcswidth('\001') == -1
        assert wcswidth('\000') == 0
        assert wcswidth('Hi \000there\000') == 8


class TestAccents:
    def test_latin1_chars(self):
        assert wcswidth('m\u00fcller') == 6

    def test_cafe(self):
        assert wcswidth('cafe\u0301') == 4

    def test_accute_accent(self):
        assert wcwidth('\u0301') == 0
        assert wcswidth('\u0301') == 0


class TestNarrowAndWide:
    def test_right_triangle(self):
        assert wcwidth('\u22bf') == 1

    def test_turned_not_sign(self):
        assert wcwidth('\u2319') == 1

    def test_watch_hourglass(self):
        assert wcwidth('\u231a') == 2
        assert wcwidth('\u231b') == 2

    def test_warning_sign(self):
        assert wcwidth('\u26a0') == 1

    def test_heavy_plus_sign(self):
        assert wcwidth('\u2795') == 2

    def test_ideographic_half_fill_space(self):
        assert wcwidth('\u303f') == 1

    def test_hiragana_small_a(self):
        assert wcwidth('\u3041') == 2

    def test_segmented_digit_three(self):
        assert wcwidth('\U0001FBF3') == 1

    def test_katakana_small_ha(self):
        assert wcwidth('\u31f5') == 2

    def test_cjk_tiger(self):
        assert wcwidth('\u4e54') == 2

    def test_hello_world_jp(self):
        assert wcswidth('コンニチハ, セカイ!') == 19

    def test_hello_world_jp_offset(self):
        assert wcswidth('コンニチハ, セカイ!', n=7) == 12


class TestBasicEmojis:
    def test_smiley(self):
        assert wcwidth('\U0001F600') == 2

    def test_hi_wave(self):
        assert wcswidth('Hi\U0001F44B!') == 5

    def test_shaking_face(self):
        assert wcwidth('\U0001FAE8') == 2


class TestFlagSequences:
    def test_french_polynesia(self):
        assert wcswidth('\U0001F1F5\U0001F1EB') == 2

    def test_diego_garcia(self):
        assert wcswidth('This is the \U0001F1E9\U0001F1EC island') == 21

    def test_scotland(self):
        assert wcswidth('\U0001F3F4\U000E0067\U000E0062\U000E0073'
                        '\U000E0063\U000E0074\U000E007F') == 2


class TestEmojiVS15VS16:
    def test_vs16_0length(self):
        assert wcwidth('\ufe0e') == 0
        assert wcswidth('\ufe0e') == 0
        assert wcwidth('\ufe0f') == 0
        assert wcswidth('\ufe0f') == 0

    def test_warn_emoji(self):
        assert wcwidth('\u26a0') == 1
        assert wcswidth('\u26a0') == 1
        assert wcswidth('\u26a0\ufe0f') == 2
        assert wcswidth('\u26a0\ufe0e') == 1
        assert wcswidth('This is a \u26a0 warning!') == 20
        assert wcswidth('This is a \u26a0\ufe0e warning!') == 20
        assert wcswidth('This is a \u26a0\ufe0f warning!') == 21

    def test_diamond_suit(self):
        assert wcwidth('\u2666') == 1
        assert wcswidth('\u2666\ufe0f') == 2
        assert wcswidth('\u2666\ufe0e') == 1

    def test_person_bouncing_ball(self):
        assert wcswidth('\u26f9') == 1
        assert wcswidth('\u26f9\ufe0f') == 2
        assert wcswidth('\u26f9\ufe0e') == 1

    def test_no_op_on_poodle(self):
        assert wcswidth('\U0001F429') == 2
        assert wcswidth('\U0001F429\ufe0f') == 2


class TestKeycaps:
    def test_five(self):
        assert wcswidth('5\ufe0f\u20e3') == 2
        assert wcswidth('5\ufe0f\u20e3 + 1 = 6') == 10


class TestEmojiModifier:
    def test_em_fitzpatrick_type_3(self):
        assert wcwidth('\U0001F3FC') == 2
        assert is_EMB('\U0001F3FC') == False
        assert is_EMB_uint32(ord('\U0001F3FC')) == False
        assert wcswidth('\U0001F3FC is a skin tone!') == 18

    def test_does_not_modify_postbox(self):
        assert wcwidth('\U0001F4EE') == 2
        assert is_EMB('\U0001F4EE') == False
        assert wcswidth('\U0001F4EE\U0001F3FE') == 4

    def test_modifies_thumb_up(self):
        assert is_EMB('\U0001F44D') == True
        assert is_EMB_uint32(ord('\U0001F44D')) == True
        assert wcswidth('\U0001F44D\U0001F3FF') == 2

    def test_does_not_modify_smiley(self):
        assert wcswidth('\U0001F600\U0001F3FB') == 4

    def test_modifies_and_emojifies_person_bouncing_ball(self):
        assert wcwidth('\u26f9') == 1
        assert is_EMB('\u26f9') == True
        assert is_EMB_uint32(ord('\u26f9')) == True
        assert wcswidth('\u26f9\U0001F3FC') == 2
        assert wcswidth('\u26f9\U0001F3FC', n=1) == 1

    def test_does_not_modify_person_bouncing_ball_vs16(self):
        assert wcswidth('\u26f9\ufe0f\U0001F3FD') == 4

    def test_does_not_modify_person_bouncing_ball_vs15(self):
        assert wcswidth('\u26f9\ufe0e\U0001F3FE') == 3

    def test_person_bouncing_ball_explained(self):
        assert wcswidth('\u26f9\U0001F3FF=\u26f9\ufe0e\U0001F3FF') == 6

    def test_does_not_modify_tent(self):
        assert wcwidth('\u26fa') == 2
        assert is_EMB('\u26fa') == False
        assert wcswidth('\u26fa\U0001F3FB') == 4

    def test_does_not_also_modify_older_chars(self):
        assert wcswidth('\u26f9\U0001F44D\U0001F3FC') == 3
        assert wcswidth('\u26f9\U0001F44D\U0001F3FC', n=1) == 1
        assert wcswidth('\u26f9\U0001F44D\U0001F3FC', n=2) == 3


class TestEmojiZWJ:
    def test_woman_with_white_cane(self):
        assert wcswidth('\U0001F469\u200d\U0001F9AF') == 2

    def test_woman_with_white_cane_facing_right(self):
        assert wcswidth('\U0001F469\u200d\U0001F9AF\u200d\u27a1') == 2

    def test_woman_with_white_cane_facing_right_fully_qualified(self):
        assert wcswidth('\U0001F469\u200d\U0001F9AF\u200d\u27a1\ufe0f') == 2

    def test_couple_with_heart_woman_man(self):
        assert wcswidth('\U0001F469\u200d\u2764\u200d\U0001F468') == 2
        assert wcswidth('\U0001F469\u200d\u2764\ufe0f\u200d\U0001F468') == 2

    def test_man_running_medium_dark_skin_tone(self):
        assert wcswidth('\U0001F3C3\U0001F3FE\u200d\u2642\ufe0f') == 2
        assert wcswidth('\U0001F3C3\U0001F3FE\u200d\u2642') == 2

    def test_kiss_person_person_medium_skin_tone_medium_dark_skin_tone(self):
        assert wcswidth('\U0001F9D1\U0001F3FD\u200d\u2764\u200d'
                        '\U0001F48B\u200d\U0001F9D1\U0001F3FE') == 2
        assert wcswidth('\U0001F9D1\U0001F3FD\u200d\u2764\ufe0f\u200d'
                        '\U0001F48B\u200d\U0001F9D1\U0001F3FE') == 2

    def test_family_man_man_girl_girl(self):
        assert wcswidth('\U0001F468\u200d\U0001F468\u200d'
                        '\U0001F467\u200d\U0001F467') == 2


class TestHard:
    def test_man_running_explained(self):
        assert wcswidth('\U0001F3C3\U0001F3FE\u200d\u2642'
                        '=\U0001F3FE\U0001F3C3\u2642') == 8
        assert wcswidth('\U0001F3C3\U0001F3FE\u200d\u2642\ufe0f'
                        '=\U0001F3C3\ufe0f\U0001F3FE\u2642') == 8

    def test_person_playing_ball_for_scotland(self):
        assert wcswidth('\u26f9\U0001F3FC'
                        '\U0001F3F4\U000E0067\U000E0062\U000E0073'
                        '\U000E0063\U000E0074\U000E007F!') == 5
        assert wcswidth('\u26f9'
                        '\U0001F3F4\U000E0067\U000E0062\U000E0073'
                        '\U000E0063\U000E0074\U000E007F!') == 4
