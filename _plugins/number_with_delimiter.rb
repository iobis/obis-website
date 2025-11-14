module Jekyll
  module NumberWithDelimiterFilter
    def number_with_delimiter(input, delimiter = ",", separator = ".")
      return input if input.nil?

      number = input.to_s
      sign = number.start_with?("-") ? "-" : ""
      number = number[1..] if sign == "-"

      integer_part, decimal_part = number.split(".", 2)
      integer_part ||= "0"

      integer_with_delimiter = integer_part.chars.reverse.each_slice(3).map(&:join).join(delimiter).reverse

      formatted = sign + integer_with_delimiter
      formatted += "#{separator}#{decimal_part}" if decimal_part && !decimal_part.empty?
      formatted
    end
  end
end

Liquid::Template.register_filter(Jekyll::NumberWithDelimiterFilter)

